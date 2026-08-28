"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

type Detection = {
  id: number;
  timestamp: string;
  image_path: string;
  confidence: number;
  status: string;
  gemini_description: string | null;
  violation_count?: number;
};

export default function Dashboard() {
  const [detections, setDetections] = useState<Detection[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = () => {
      fetch("/api/detections?limit=100")
        .then((res) => res.json())
        .then((data) => {
          setDetections(data);
          setLoading(false);
        })
        .catch((err) => {
          console.error(err);
          setLoading(false);
        });
    };

    // Initial fetch
    fetchData();

    // Poll every 3 seconds
    const interval = setInterval(fetchData, 3000);
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status: string) => {
    if (status === "CONFIRMED_BY_YOLO") return "default";
    if (status === "CONFIRMED_BY_GEMINI") return "destructive";
    if (status === "PENDING_GEMINI") return "secondary";
    return "outline"; // REJECTED
  };
  
  const getStatusText = (status: string) => {
    if (status === "CONFIRMED_BY_YOLO") return "YOLO Confirmed";
    if (status === "CONFIRMED_BY_GEMINI") return "Gemini Confirmed";
    if (status === "PENDING_GEMINI") return "Verifying...";
    return "Rejected";
  };

  const getFilename = (path: string) => {
    return path.split('\\').pop() || path.split('/').pop() || "";
  };

  // Generate chart data based on hour of day
  const chartData = Array.from({ length: 24 }).map((_, i) => ({
    hour: `${i}:00`,
    count: 0
  }));
  
  detections.forEach(d => {
    const date = new Date(d.timestamp + "Z"); // SQLite gives UTC without Z
    const hour = date.getHours();
    if (d.status.includes("CONFIRMED")) {
      chartData[hour].count += (d.violation_count ?? 1);
    }
  });

  const totalViolations = detections
    .filter(d => d.status.includes("CONFIRMED"))
    .reduce((sum, d) => sum + (d.violation_count ?? 1), 0);
  const pendingVerifications = detections.filter(d => d.status === "PENDING_GEMINI").length;

  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">CCTV Helmet Detection Dashboard</h2>
      </div>
      
      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="gallery">Evidence Gallery</TabsTrigger>
        </TabsList>
        
        <TabsContent value="overview" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Violations</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{loading ? "..." : totalViolations}</div>
                <p className="text-xs text-muted-foreground">Detected so far</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Pending Verifications</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{loading ? "..." : pendingVerifications}</div>
                <p className="text-xs text-muted-foreground">Waiting for Gemini AI</p>
              </CardContent>
            </Card>
          </div>
          
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
            <Card className="col-span-4">
              <CardHeader>
                <CardTitle>Daily Trends (Peak Hour)</CardTitle>
              </CardHeader>
              <CardContent className="pl-2">
                <div className="h-[350px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData}>
                      <XAxis dataKey="hour" stroke="#888888" fontSize={12} tickLine={false} axisLine={false} />
                      <YAxis stroke="#888888" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `${value}`} />
                      <Tooltip />
                      <Bar dataKey="count" fill="currentColor" radius={[4, 4, 0, 0]} className="fill-primary" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
            
            <Card className="col-span-3">
              <CardHeader>
                <CardTitle>Recent Detections</CardTitle>
                <CardDescription>Latest events from the CCTV stream</CardDescription>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Time</TableHead>
                      <TableHead>Confidence</TableHead>
                      <TableHead>Status</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {detections.slice(0, 5).map((detection) => {
                       const d = new Date(detection.timestamp + "Z");
                       return (
                        <TableRow key={detection.id}>
                          <TableCell className="font-medium">{d.toLocaleTimeString()}</TableCell>
                          <TableCell>{(detection.confidence * 100).toFixed(1)}%</TableCell>
                          <TableCell>
                            <Badge variant={getStatusColor(detection.status) as any}>
                              {getStatusText(detection.status)}
                            </Badge>
                          </TableCell>
                        </TableRow>
                      );
                    })}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
        
        <TabsContent value="gallery" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {detections.filter(d => d.status !== "REJECTED").map((detection) => {
              const filename = getFilename(detection.image_path);
              const imageUrl = `/api/evidence?file=${encodeURIComponent(filename)}`;
              const d = new Date(detection.timestamp + "Z");
              
              return (
                <Card key={detection.id} className="overflow-hidden">
                  <div className="aspect-video relative overflow-hidden bg-slate-100">
                    <img 
                      src={imageUrl} 
                      alt="Evidence" 
                      className="object-cover w-full h-full"
                      onError={(e) => {
                        (e.target as HTMLImageElement).src = "https://placehold.co/600x400?text=Image+Not+Found";
                      }}
                    />
                  </div>
                  <CardHeader className="p-4 pb-2">
                    <div className="flex justify-between items-start">
                      <CardTitle className="text-base">{d.toLocaleString()}</CardTitle>
                      <Badge variant={getStatusColor(detection.status) as any}>
                        {getStatusText(detection.status)}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent className="p-4 pt-0 text-sm text-muted-foreground">
                    {detection.gemini_description ? (
                      <p className="line-clamp-3" title={detection.gemini_description}>
                        <span className="font-semibold text-foreground">AI Analysis:</span> {detection.gemini_description}
                      </p>
                    ) : (
                      <p>Detected by YOLO Edge AI. Confidence: {(detection.confidence * 100).toFixed(1)}%</p>
                    )}
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
