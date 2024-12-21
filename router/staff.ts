import * as express from "express";
import axios from "axios";
import Staff from "../mongoose_schemas/staff";

const router = express.Router();

router.get   ("/staffs", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get   ("http://pythonserver:27018/staffs");
        res.json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get   ("/staff", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get   (`http://pythonserver:27018/staff?id=${req.query.id}`);
        res.json(response.data);
    } catch (err) {
        next(err);
    }
});

router.post  ("/staff", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.post  ("http://pythonserver:27018/staff"                  , req.body);
        res.json(response.data);        
    } catch (err) {
        next(err);
    }
});

router.put   ("/staff", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.put   (`http://pythonserver:27018/staff?id=${req.query.id}`, req.body);
        res.json(response.data);    
    } catch (err) {
        next(err);
    }
});

router.delete("/staff", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.delete(`http://pythonserver:27018/staff?id=${req.query.id}`);
        res.json(response.data);    
    } catch (err) {
        next(err);
    }
});

router.post("/get-staff-by-user-id", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const staff = await Staff.findOne({ userId: req.body.userId });
        res.json({ "staff": staff });
    } catch (err) {
        next(err);
    }
});

router.get("/staff/row", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/staff/row?numberRowIgnore=${req.query.numberRowIgnore}`);
        res.json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/staff/search", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/staff/search?search=${req.query.search}&numberRowIgnore=${req.query.numberRowIgnore}`);
        res.json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/staffs/count", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/staffs/count`);
        res.json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/staff/search/count", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/staff/search/count?search=${req.query.search}&numberRowIgnore=${req.query.numberRowIgnore}`);
        res.json(response.data);
    } catch (err) {
        next(err);
    }
});

export default router;
