import * as express from "express";
import * as path from "path";
import redisClient from "./redisClient";
import mongoClient from "./mongoClient";
import authRoute from "./router/auth";
import orderRoute from "./router/order";
import passport  from "./passportJwt";
import { ensureUserExists } from "./mongoose_schemas/user";

redisClient.connect();
mongoClient.connect();

const app = express();
const port = parseInt(process.env.PORT) || process.argv[3] || 8088;

app.use(express.static(path.join(__dirname, "public")))
  .set("views", path.join(__dirname, "views"))
  .set("view engine", "ejs");

const   bodyParser = require("body-parser");
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json())

app.use( passport .initialize());
app.use( ensureUserExists );
app.use("/auth", authRoute);
app.use("/protected", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
  passport.authenticate("jwt", { session: false }, (err, user, info, status) => {
    if (!user || err) return res.status(403).json({ "msg": info });
    res.locals.user = user;
    next();
  })(req,
     res,
    next) ;
});
app.use("/order", orderRoute);

app.get("/"   , async (req: express.Request, res: express.Response, next: express.NextFunction) => {
  res.json({ "msg": "Hello 1" });
});

app.get("/api", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
  res.json({ "msg": "Hello 2" });
});

app.get("/protected/profile", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
  res.json({ "msg":"Profile", "data":res.locals.user });
});

// app.get("/save-user", async (req, res) => {
//   const instance = new User();
//   instance.username = "test";
//   instance.password = "test";
//   await instance.save();
//   res.json({ "msg": await User.find({}) });
// });

// app.get("/load-user", async (req, res) => {
//   res.json({ "msg": await User.find({}) });
// });
import axios from "axios";
app.get("/health", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
  const response = await axios.get("http://pythonserver:27018/health");
  res.json(response.data);
});

app.get ("/classify-image", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
  const response = await axios.get ("http://pythonserver:27018/classify-image");
  res.json(response.data);
});

app.post("/classify-image", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
  const response = await axios.post("http://pythonserver:27018/classify-image", {
    data: {
      image_url:req.body.image_url
    }
  });
  res.json(response.data);
});

app.get ("/chat", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
  const response = await axios.get ("http://pythonserver:27018/chat");
  res.json(response.data);
});

app.post("/chat", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
  const response = await axios.post(`http://pythonserver:27018/chat?prompt=${req.query.prompt}`);
  res.json(response.data);
});

app.listen(port, () => {
  console.log(`Listening on http://localhost:${port}`);
});
