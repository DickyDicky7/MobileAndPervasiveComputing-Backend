import * as express from "express";
import axios from "axios";

const router = express.Router();

router.get   ("/hubs", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    const response = await axios.get   ("http://pythonserver:27018/hubs");
    res.json(response.data);
});

router.get   ("/hub", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    const response = await axios.get   (`http://pythonserver:27018/hub?id=${req.query.id}`);
    res.json(response.data);
});

router.post  ("/hub", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    const response = await axios.post  ("http://pythonserver:27018/hub"                  , req.body);
    res.json(response.data);
});

router.put   ("/hub", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    const response = await axios.put   (`http://pythonserver:27018/hub?id=${req.query.id}`, req.body);
    res.json(response.data);
});

router.delete("/hub", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    const response = await axios.delete(`http://pythonserver:27018/hub?id=${req.query.id}`);
    res.json(response.data);
});

export default router;
