import * as express from "express";
import axios    from "axios";
import mongoose from "mongoose";
import Order, { ShipmentType, DeliveryType } from "../mongoose_schemas/order";

const router = express.Router();

router.post("/confirmation", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {


    const {   senderInfo,
            receiverInfo,
            deliveryInfo,
              hubId,
            message,
            payStatus,
            payWith  ,
        } = req.body;
    if (!Object.values(ShipmentType).includes(deliveryInfo.shipmentType)) {
        return res.status(400).json({"msg": "Shipments type not found" });
    }
    if (!Object.values(DeliveryType).includes(deliveryInfo.deliveryType)) {
        return res.status(400).json({ "msg": "Delivery type not found" });
    }
    try {
        const newOrder = new Order({
              senderInfo:   senderInfo,
            receiverInfo: receiverInfo,
            deliveryInfo: deliveryInfo,
              hubId: new mongoose.Types.ObjectId(hubId),
            message: message,
            podTxt : "",
            podImg : "",
            payStatus: payStatus,
            payWith  : payWith  ,
        })
        const savedOrder = await newOrder.save();
        return res.status(201).json({ 
            "msg": "Order confirmed!",
            "orderId": savedOrder._id,
            "order##": savedOrder    ,
        });
    }
    catch (err) {
        return res.status(500).json({ "msg": "Order confirmation API goes something wrong/unknown", "err": err });
    }


    } catch (err) {
        next(err);
    }
});

router.get   ("/orders", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get   ("http://pythonserver:27018/orders");
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get   ("/order", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get   (`http://pythonserver:27018/order?id=${req.query.id}`);
        res.status(response.status).json(response.data);    
    } catch (err) {
        next(err);
    }
});

router.post  ("/order", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.post  ("http://pythonserver:27018/order"                  , req.body);
        res.status(response.status).json(response.data);    
    } catch (err) {
        next(err);
    }
});

router.put   ("/order", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.put   (`http://pythonserver:27018/order?id=${req.query.id}`, req.body);
        res.status(response.status).json(response.data);    
    } catch (err) {
        next(err);
    }
});

router.delete("/order", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.delete(`http://pythonserver:27018/order?id=${req.query.id}`);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/orders/sender", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/orders/sender?userId=${req.query.userId}`);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/orders/receiver", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/orders/receiver?userId=${req.query.userId}`);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/orders/hub", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/orders/hub?hubId=${req.query.hubId}`);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

router.put("/order/payStatus", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.put(`http://pythonserver:27018/order/payStatus?id=${req.query.id}&payStatus=${req.query.payStatus}`);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

router.put("/order/devStatus", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const          {
             orderId
//      ,    devStatus
//      ,    payStatus
                       } = req.body;

        if (!orderId  ) {
            return res.status(400).json({ msg: "bad request - orderId   is required" });
        }

//      if (!devStatus) {
//          return res.status(400).json({ msg: "bad request - devStatus is required" });
//      }

//      if (!payStatus) {
//          return res.status(400).json({ msg: "bad request - payStatus is required" });
//      }

        const order =  await Order.findById(new mongoose.Types.ObjectId(orderId));
        if ( !order ) {
            return res.status(400).json({ msg: "your order not found" });
        }
        if (order.payWith   === "cash"
        &&  order.payStatus === "pending") {
            order.payStatus =   "success";
        } else {
            order.payStatus =
            order.payStatus ;
        }
        if (order.deliveryInfo.status === "pending") {
            order.deliveryInfo.status = 
                  "inProgress";
        } else
        if (order.deliveryInfo.status ===
                              "failed"             ) {
            order.deliveryInfo.status =               "canceled";
        } else {
            order.deliveryInfo.status = 
            order.deliveryInfo.status ;
        }
        await order.save();
        return res.status(200).json({ order: order });
    } catch (err) {
        next(err);
    }
});

router.get("/order/row", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/order/row?numberRowIgnore=${req.query.numberRowIgnore}`);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/order/search", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/order/search?search=${req.query.search}&numberRowIgnore=${req.query.numberRowIgnore}`);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/orders/count", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/orders/count`);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/order/search/count", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/order/search/count?search=${req.query.search}&numberRowIgnore=${req.query.numberRowIgnore}`);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

export default router;


