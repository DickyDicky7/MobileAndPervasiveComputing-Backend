import * as express from "express";
import axios from "axios";

const router = express.Router();

router.get   ("/hubs", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get   ("http://pythonserver:27018/hubs");
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get   ("/hub", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get   (`http://pythonserver:27018/hub?id=${req.query.id}`);
        res.status(response.status).json(response.data);    
    } catch (err) {
        next(err);
    }
});

router.post  ("/hub", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.post  ("http://pythonserver:27018/hub"                  , req.body);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

router.put   ("/hub", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.put   (`http://pythonserver:27018/hub?id=${req.query.id}`, req.body);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

router.delete("/hub", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.delete(`http://pythonserver:27018/hub?id=${req.query.id}`);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/hub/near", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.delete(`http://pythonserver:27018/hub/near?address=${req.query.address}`);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/hub/row", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/hub/row?numberRowIgnore=${req.query.numberRowIgnore}`);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/hubs/search", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/hubs/search?search=${req.query.search}`);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/hub/search", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/hub/search?search=${req.query.search}&numberRowIgnore=${req.query.numberRowIgnore}`);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/hubs/count", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/hubs/count`);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/hub/search/count", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/hub/search/count?search=${req.query.search}&numberRowIgnore=${req.query.numberRowIgnore}`);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

export default router;
