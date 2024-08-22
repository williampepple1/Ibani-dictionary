import express, { Request, Response } from 'express';
import sqlite3 from 'sqlite3';
import { open } from 'sqlite';

const app = express();
const port = 3000;

async function openDB() {
  return open({
    filename: './IbaniDictionary.db',
    driver: sqlite3.Database
  });
}

app.get('/search', async (req: Request, res: Response) => {
  const searchTerm = req.query.word as string;

  if (!searchTerm) {
    return res.status(400).json({ error: 'A search word must be provided' });
  }

  try {
    const db = await openDB();
    const result = await db.get('SELECT * FROM dictionary WHERE name = ?', searchTerm.toLowerCase());

    if (!result) {
      return res.status(404).json({ error: 'Word not found' });
    }

    res.json(result);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Database query failed' });
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
