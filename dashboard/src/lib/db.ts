import sqlite3 from 'sqlite3';
import path from 'path';

// Construct path to the SQLite database relative to the dashboard directory
const dbPath = path.resolve(process.cwd(), '../data/helmet_detection.db');

export function getDbConnection() {
  return new sqlite3.Database(dbPath, (err) => {
    if (err) {
      console.error('Error opening database', err.message);
    }
  });
}

export function query(sql: string, params: any[] = []): Promise<any[]> {
  return new Promise((resolve, reject) => {
    const db = getDbConnection();
    db.all(sql, params, (err, rows) => {
      if (err) {
        reject(err);
      } else {
        resolve(rows);
      }
      db.close();
    });
  });
}
