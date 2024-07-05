import * as express from "express";
import axios from "axios";

const router = express.Router();

router.get ("/classify-image", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
  try {
    const response = await axios.get ("http://pythonserver:27018/classify-image");
    res.json(response.data);
  } catch (err) {
    next  (err);
  }
});

router.post("/classify-image", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
  try {
    const response = await axios.post("http://pythonserver:27018/classify-image", {
      image_url : req.body.image_url
    });
    res.json(response.data);
  } catch (err) {
    next  (err);
  }
});

router.get ("/chat", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
  try {
    const response = await axios.get ("http://pythonserver:27018/chat");
    res.json(response.data);
  } catch (err) {
    next  (err);
  }
});

router.post("/chat", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
  try {
    const response = await axios.post(`http://pythonserver:27018/chat?prompt=${req.query.prompt}`);
    res.json(response.data);  
  } catch (err) {
    next  (err);
  }
});

router.get ("/recommendation", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
  try {
    const response = await axios.get ("http://pythonserver:27018/recommendation");
    res.json(response.data);  
  } catch (err) {
    next  (err)
  }
});

router.post("/recommendation", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
  try {
    const response = await axios.post("http://pythonserver:27018/recommendation", {
      category  : req.body.category
    });
    res.json(response.data);
  } catch (err) {
    next  (err)
  }
});

router.get ("/extract-text-from-image", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
  try {
    const response = await axios.get ("http://pythonserver:27018/extract-text-from-image");
    res.json(response.data);  
  } catch (err) {
    next  (err);
  }
});

router.post("/extract-text-from-image", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
  try {
    const response = await axios.post("http://pythonserver:27018/extract-text-from-image", {
      image_url : req.body.image_url
    });
    res.json(response.data);
  } catch (err) {
    next  (err);
  }
});

export default router;