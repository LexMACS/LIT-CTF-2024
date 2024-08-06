import express from "express";
import path from "node:path";
import { scramble, size } from "./generate";
import bodyParser from "body-parser";
import fs from "node:fs";

const { scrambled, unscrambled } = scramble();

const app = express();
app.use(bodyParser.json({ limit: "2mb" }));

app.get("/", (_, res) => {
  return res.sendFile(path.join(__dirname, "index.html"));
});

app.get("/data", (_, res) => {
  return res.json(scrambled);
});

app.post("/test", (req, res) => {
  const { data } = req.body;
  if (!data) {
    return res.status(400).send("No data provided");
  }

  if (!Array.isArray(data) || data.length > size * size) {
    return res
      .status(400)
      .send(
        "Invalid data (the array might be too long, don't give me too many steps!)"
      );
  }
  const s = [...scrambled];
  const swaps = [...data];
  for (let i = 0; i < swaps.length; i++) {
    const [a, b] = swaps[i];
    [s[a], s[b]] = [s[b], s[a]];
  }

  console.log("eeeee", swaps.length);

  if (s.every((v, i) => v === unscrambled[i])) {
    return res.send(fs.readFileSync(path.join(__dirname, "flag.txt"), "utf-8"));
  } else {
    return res.send("Incorrect! try again!");
  }
});

app.get("/gridsize", (_, res) => {
  res.send(`${size}`);
});

const port = process.env.PORT || 3000;

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
