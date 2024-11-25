import * as express from "express";
import * as path from "path";
import axios from "axios";
import redisClient from "./redisClient";
import mongoClient from "./mongoClient";
import  authRoute from "./router/auth" ;
import orderRoute from "./router/order";
import   hubRoute from "./router/hub"  ;
import   a_iRoute from "./router/a.i"  ;
import staffRoute from "./router/staff";
import   assignRoute from "./router/assign"  ;
import deliveryRoute from "./router/delivery";
import passport  from "./passportJwt";
import { ensureUserExists, getUserIdByUsername } from "./mongoose_schemas/user";
import { getOrdersByUserIdAndStatus, getOrderByUserIdAndType } from "./mongoose_schemas/order";

redisClient.connect();
mongoClient.connect();

const app  = express();
const port = parseInt(process.env.PORT) || process.argv[3] || 8088;

app.use(express.static(path.join(__dirname, "public")))
  .set("views", path.join(__dirname, "views"))
  .set("view engine", "ejs");

const   bodyParser = require("body-parser");
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json({ limit:  "100mb" }));

const       morgan = require(     "morgan");
app.use(    morgan("tiny"));

app.use( passport .initialize());
app.use( ensureUserExists );
var hasInit = false;
// app.use(async (req: express.Request, res: express.Response, next: express.NextFunction) => {
//   if (!hasInit) {
//     await axios.get("http://pythonserver:27018/init");
//     hasInit = true;
//   }
//   next();
// });
const swaggerUi       = require("swagger-ui-express"                      );
const swaggerDocument = require(                   "./swagger-output.json");

app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerDocument));
app.use("/auth", authRoute);
app.use("/protected", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
  
  return next();///
  
  passport.authenticate("jwt", { session: false }, (err, user, info, status) => {
    if (!user || err) return res.status(403).json({ "msg": info });
    res.locals.user = user;
    next();
  })(req,
    res,
    next) ;
  });
  app.use("/protected", orderRoute);
  app.use("/protected",   hubRoute);
  app.use("/protected",   a_iRoute);
  app.use("/protected", staffRoute);
  app.use("/protected",   assignRoute);
app.use("/protected", deliveryRoute);

  app.get("/"   , async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    res.json({ "msg": "Hello 1" });
  });
  
  app.get("/api", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    res.json({ "msg": "Hello 2" });
  });
  
  app.get("/protected/profile", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    res.json({ "msg":"Profile", "data":res.locals.user });
  });
  app.post("/getUserIdByUsername"      , getUserIdByUsername       );
  app.post("/getOrderByUserIdAndStatus", getOrdersByUserIdAndStatus);
  app.post("/getOrderByUserIdAndType"  , getOrderByUserIdAndType);
  
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
      
      // import axios from "axios";
      app.get("/health", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
        const response = await axios.get("http://pythonserver:27018/health");
        res.json(response.data);
      });
      
      // app.get ("/protected/classify-image", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
        //   const response = await axios.get ("http://pythonserver:27018/classify-image");
//   res.json(response.data);
// });

// app.post("/protected/classify-image", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
  //   const response = await axios.post("http://pythonserver:27018/classify-image", {
    //     image_url : req.body.image_url
    //   });
    //   res.json(response.data);
    // });
    
    // app.get ("/protected/chat", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
      //   const response = await axios.get ("http://pythonserver:27018/chat");
      //   res.json(response.data);
      // });
      
      // app.post("/protected/chat", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
        //   const response = await axios.post(`http://pythonserver:27018/chat?prompt=${req.query.prompt}`);
//   res.json(response.data);
// });

// app.get ("/protected/recommendation", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
//   const response = await axios.get ("http://pythonserver:27018/recommendation");
//   res.json(response.data);
// });

// app.post("/protected/recommendation", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
//   const response = await axios.post("http://pythonserver:27018/recommendation", {
//     category  : req.body.category
//   });
//   res.json(response.data);
// });

// app.get ("/protected/extract-text-from-image", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
//   const response = await axios.get ("http://pythonserver:27018/extract-text-from-image");
//   res.json(response.data);
// });

// app.post("/protected/extract-text-from-image", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
//   const response = await axios.post("http://pythonserver:27018/extract-text-from-image", {
//     image_url : req.body.image_url
//   });
//   res.json(response.data);
// });

app.listen(port, () => {
  console.log(`Listening on http://localhost:${port}`);
});

import mongoose from "mongoose";
app.get("/nuke", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
  try {
    // throw new Error("test");
    await Promise.all(Object.values(mongoose.connection.collections).map((collection) =>
       collection.deleteMany({})
    ));
    res.status(200).json({ "msg": "ok" });
  } catch (err) {
    res.status(500).json({ "msg": err, });
  }
});

// app.use(async (err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
//   console.log (err);
// res.status(500).json({ "msg": err });
// });

import Staff from "./mongoose_schemas/staff";
import Hub   from "./mongoose_schemas/hub"  ;
import Order from "./mongoose_schemas/order";
import User from "./mongoose_schemas/user";
app.get("/init", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
  const shipper1 = await User.findOne({ username: "sh1" });
  const shipper2 = await User.findOne({ username: "sh2" });
  const client1 = await User.findOne({ username: "cl1" });
  const client2 = await User.findOne({ username: "cl2" });
  const client3 = await User.findOne({ username: "cl3" });
  const client4 = await User.findOne({ username: "cl4" });
  const hub1 = new Hub({
    name: "Hub 1",
    address: "Hẻm 196 Lê Thị Bạch Cát, Ho Chi Minh City, Ho Chi Minh 72000, Vietnam",
  });
  const hub2 = new Hub({
    name: "Hub 2",
    address: "Đường Nguyễn Án, Ho Chi Minh City, Ho Chi Minh, Vietnam"    ,
  });
  await hub1.save();
  await hub2.save();
  const order1 = new Order({
      senderInfo: { name:   "Sender1", address: "-", phoneNumber: 0, userId: client1._id },
    receiverInfo: { name: "Receiver1", address: "-", phoneNumber: 0, userId: client3._id },
    deliveryInfo: { 
      shipmentType: "Package" ,
      deliveryType: "Standard",
      status      : "pending" ,
      packageSize :          50 ,
      pickupDate  : "2024-01-01",
      pickupTime  : "12:30" ,
      value       :  1200000,
    },
    hubId  : hub1._id,
    message: "-"     ,
  });
  const order2 = new Order({
    
      senderInfo: { name:   "Sender2", address: "-", phoneNumber: 0, userId: client2._id },
    receiverInfo: { name: "Receiver2", address: "-", phoneNumber: 0, userId: client4._id },
    deliveryInfo: {
      shipmentType: "Package" ,
      deliveryType: "Standard",
      status      : "pending" ,
      packageSize :          30 ,
      pickupDate  : "2024-01-01",
      pickupTime  : "12:30",
      value       :  800000,  
    },
    hubId  : hub1._id,
    message: "-"     ,
  });
  await order1.save();
  await order2.save();
  const staff1 = new Staff({
    name  : "John Doeee",
    age   : 25    ,
    gender: "male",
    weight: 70    ,
    motorcycleCapacity: 150,
     hubId:     hub1._id,
    userId: shipper1._id,
  });
  const staff2 = new Staff({
    name   : "Jane Smith",
    age   : 30      ,
    gender: "female",
    weight: 60      ,
    motorcycleCapacity: 100,
     hubId:     hub1._id,
    userId: shipper2._id,
  });
  await staff1.save();
  await staff2.save();
  res.status(200).json({
    "initData": [
      hub1,
      hub2,
      order1,
      order2,
      staff1,
      staff2,
    ]
  });
});

app.get("/checkgeo", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
  try {
    const response = await axios.get("http://pythonserver:27018/checkgeo");
    res.json(response.data);
  } catch (err) {
    next  (err);
  }
})


import { createClient } from "@supabase/supabase-js";
import { decode       } from    "base64-arraybuffer";
// Create a single supabase client for interacting with your database
const supabase = createClient("https://fdahwnwelowronwevgty.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZkYWh3bndlbG93cm9ud2V2Z3R5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzIyNDM5ODEsImV4cCI6MjA0NzgxOTk4MX0.bWacxK5VWlAWEh6V-mp4FUgAhya0w1hDb9bKUmmulvk");
// const imgbbUploader = require("imgbb-uploader");
app.post("/up-img", async (req: express.Request, res: express.Response  , next: express.NextFunction) => {
  try {
    // const byteArray: Uint8Array = new Uint8Array(req.body.image);
    // const       buffer = Buffer.from                 (byteArray);
    // const base64String = buffer.toString("base64");
    // const options = {
    //   apiKey: "2b1cc30f70dd96ab10f68948f74b6f06",
    //   name  : req.body.imageName,
    //   base64string: base64String,
    // };
    // imgbbUploader(options).then((response) => { console.log(response); res.json({ "data": response }); }).catch((error) => { console.error(error); res.json({ "data": error }); });

    const { data, error } = await supabase.storage
      .from("abc")
      .upload(`${req.body.imageName}.jpg`, decode(req.body.image), {
        contentType: "image/jpg"
      });

    const realData = supabase.storage
      .from("abc")
      .getPublicUrl(`${req.body.imageName}.jpg`);

    res.json({ "data": data, "error": error, "realData": realData.data });

  } catch (err) {
    next  (err);
  }
});

app.use(async (err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.debug(err);
  res.status(500).json({ "msg": err });
});

























