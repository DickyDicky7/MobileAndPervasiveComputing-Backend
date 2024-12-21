import * as express from "express";
import axios from "axios";
import mongoose from "mongoose";

const router = express.Router();

router.post("/delivery/update_status", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.post("http://pythonserver:27018/delivery/update_status", req.body);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/delivery/id", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/delivery/id?deliveryId=${req.query.deliveryId}`);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/deliveries", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/deliveries`);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/deliveries/hub", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/deliveries/hub?hubId=${req.query.hubId}`);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/deliveries/staff", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/deliveries/staff?staffId=${req.query.staffId}`);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/delivery/row", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/delivery/row?numberRowIgnore=${req.query.numberRowIgnore}`);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/delivery/search", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/delivery/search?search=${req.query.search}&numberRowIgnore=${req.query.numberRowIgnore}`);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/deliveries/count", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/deliveries/count`);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/delivery/search/count", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/delivery/search/count?search=${req.query.search}&numberRowIgnore=${req.query.numberRowIgnore}`);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

export default router;
