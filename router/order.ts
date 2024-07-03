import * as express from "express";
import axios    from "axios";
import mongoose from "mongoose";
import Order, { ShipmentType, DeliveryType } from "../mongoose_schemas/order";

const router = express.Router();

router.post("/confirmation", async (req: express.Request, res: express.Response, next: express.RequestHandler) =>{
    const { shipmentType,
            deliveryType,
              senderInfo,
            receiverInfo,
            packageSize,
            weight,
            status,
            pickupDate,
            pickupTime,
            value,
            hubId,
            deliveryAddress,
                    message,
            inProgress,
        } = req.body;
    if (!Object.values(ShipmentType).includes(shipmentType)){
        return res.status(400).json({"msg": "Shipment type not found"});
    }
    if (!Object.values(DeliveryType).includes(deliveryType)) {
        return res.status(400).json({ "msg": "Delivery type not found" });
    }
    try {
        const newOrder = new Order({
            shipmentType: shipmentType,
            deliveryType: deliveryType,
              senderInfo:   senderInfo,
            receiverInfo: receiverInfo,
            weight      : weight,
            status      : status,
            packageSize : packageSize,
            pickupDate  : pickupDate,
            pickupTime  : pickupTime,
            value: value,
            hubId: new mongoose.Types.ObjectId(hubId),
            deliveryAddress: deliveryAddress,
                    message:         message,
            inProgress: inProgress,
        })
        await newOrder.save();
        return res.status(201).json({ "msg": "Order confirmed!" });
    }
    catch {
        return res.status(500).json({ "msg": "Order confirmation API goes something wrong/unknown" });
    }
});

router.get   ("/orders", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    const response = await axios.get   ("http://pythonserver:27018/orders");
    res.json(response.data);
});

router.get   ("/order", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    const response = await axios.get   (`http://pythonserver:27018/order?id=${req.query.id}`);
    res.json(response.data);
});

router.post  ("/order", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    const response = await axios.post  ("http://pythonserver:27018/order"                  , req.body);
    res.json(response.data);
});

router.put   ("/order", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    const response = await axios.put   (`http://pythonserver:27018/order?id=${req.query.id}`, req.body);
    res.json(response.data);
});

router.delete("/order", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    const response = await axios.delete(`http://pythonserver:27018/order?id=${req.query.id}`);
    res.json(response.data);
});

export default router;


