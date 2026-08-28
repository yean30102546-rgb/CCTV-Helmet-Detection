import { NextResponse } from 'next/server';
import { query } from '@/lib/db';

export const dynamic = 'force-dynamic';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const limit = searchParams.get('limit') || '50';
    
    const sql = `
      SELECT * FROM detections 
      ORDER BY timestamp DESC 
      LIMIT ?
    `;
    
    const rows = await query(sql, [limit]);
    
    return NextResponse.json(rows);
  } catch (error: any) {
    console.error('API Error:', error);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
