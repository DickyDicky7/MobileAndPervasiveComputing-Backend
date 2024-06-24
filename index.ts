import * as express from "express";
import * as path from "path";
import redisClient from "./redisClient";
import mongoClient from "./mongoClient";
import User from "./mongoose_schemas/user"

redisClient.connect();
mongoClient.connect();

const app = express();
const port = parseInt(process.env.PORT) || process.argv[3] || 8080;

app.use(express.static(path.join(__dirname, "public")))
  .set("views", path.join(__dirname, "views"))
  .set("view engine", "ejs");

app.get("/", async (req, res) => {
  // redisClient.flushAll();
  if (await redisClient.get("some-key") === null) {
    await redisClient.set("some-key", "value");
    res.json({ "answer": "key - value not found, oh no!!!" });
    // return;
  }
  else {
    res.json({ "answer": "key - value found, yeah baby!!!" });
    // return;
  }
  // redisClient.flushAll();
  return;
  // res.render("index");
});

app.get("/api", async (req, res) => {
  res.json({ "msg": "Hello world" });
});

app.get("/save-user", async (req, res) => {
  const instance = new User();
  instance.username = "test";
  instance.password = "test";
  await instance.save();
  res.json({ "msg": await User.find({}) });
});

app.get("/load-user", async (req, res) => {
  res.json({ "msg": await User.find({}) });
});

app.listen(port, () => {
  console.log(`Listening on http://localhost:${port}`);
});
