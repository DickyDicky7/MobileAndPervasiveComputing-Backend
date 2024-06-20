import * as express from "express";
import * as path from "path";
import * as redis from "redis";

const redisClient = redis.createClient();
redisClient.on("connect", () => {
  console.log("Redis connected");
});
redisClient.on("error", (err) => {
  console.log("Redis error:", err);
});
redisClient.connect();

const app = express();
const port = parseInt(process.env.PORT) || process.argv[3] || 8080;

app.use(express.static(path.join(__dirname, 'public')))
  .set('views', path.join(__dirname, 'views'))
  .set('view engine', 'ejs');

app.get('/', async (req, res) => {
  if (await redisClient.get("some-key") === null) {
    await redisClient.set("some-key", "value");
    res.json({ "answer": "key - value not found, oh no!" });
    return;
  }
  else {
    res.json({ "answer": "key - value found, yeah baby!" });
    return;
  }
  // res.render('index');
});

app.get('/api', async (req, res) => {
  res.json({ "msg": "Hello world" });
});

app.listen(port, () => {
  console.log(`Listening on http://localhost:${port}`);
});
