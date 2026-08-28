import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const filename = searchParams.get('file');
    
    if (!filename) {
      return new NextResponse("Filename is required", { status: 400 });
    }
    
    // Construct absolute path to the data/evidence folder
    const evidenceDir = path.resolve(process.cwd(), '../data/evidence');
    const filePath = path.join(evidenceDir, filename);
    
    // Security check to prevent directory traversal
    if (!filePath.startsWith(evidenceDir)) {
      return new NextResponse("Invalid file path", { status: 403 });
    }
    
    if (!fs.existsSync(filePath)) {
      return new NextResponse("Image not found", { status: 404 });
    }
    
    const imageBuffer = fs.readFileSync(filePath);
    
    return new NextResponse(imageBuffer, {
      headers: {
        'Content-Type': 'image/jpeg',
        'Cache-Control': 'public, max-age=86400',
      },
    });
  } catch (error: any) {
    console.error('Evidence API Error:', error);
    return new NextResponse(error.message, { status: 500 });
  }
}
