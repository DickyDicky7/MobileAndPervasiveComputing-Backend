import * as express from "express";
import axios from                    "axios";
import User  from "../mongoose_schemas/user";

const router = express.Router();


router.get   ("/users", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get   ("http://pythonserver:27018/users");
        res.json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get   ("/user", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get   (`http://pythonserver:27018/user?id=${req.query.id}`);
        res.json(response.data);
    } catch (err) {
        next(err);
    }
});

router.post  ("/user", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.post  ("http://pythonserver:27018/user"                  , req.body);
        res.json(response.data);        
    } catch (err) {
        next(err);
    }
});

router.put   ("/user", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.put   (`http://pythonserver:27018/user?id=${req.query.id}`, req.body);
        res.json(response.data);    
    } catch (err) {
        next(err);
    }
});

router.delete("/user", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.delete(`http://pythonserver:27018/user?id=${req.query.id}`);
        res.json(response.data);    
    } catch (err) {
        next(err);
    }
});

router.get("/user/row", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/user/row?numberRowIgnore=${req.query.numberRowIgnore}`);
        res.json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/users/search", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/users/search?search=${req.query.search}`);
        res.json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/user/search", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/user/search?search=${req.query.search}&numberRowIgnore=${req.query.numberRowIgnore}`);
        res.json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/users/count", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/users/count`);
        res.json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/user/search/count", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/user/search/count?search=${req.query.search}&numberRowIgnore=${req.query.numberRowIgnore}`);
        res.json(response.data);
    } catch (err) {
        next(err);
    }
});

export default router;
