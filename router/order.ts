import * as express from "express";
import Order, { ShipmentType, DeliveryType } from "../mongoose_schemas/order";

const router = express.Router();

router.post("/confirmation", async (req: express.Request, res: express.Response, next: express.RequestHandler) => {
    const { shipmentType, deliveryType, senderInfo, receiverInfo, pickupDate, pickupTime } = req.body;
    if (!Object.values(ShipmentType).includes(shipmentType)) {
        return res.status(400).json({ "msg": "Shipment type not found" });
    }
    if (!Object.values(DeliveryType).includes(deliveryType)) {
        return res.status(400).json({ "msg": "Delivery type not found" });
    }
    try {
        const newOrder = new Order({
            shipmentType: shipmentType,
            deliveryType: deliveryType,
            senderInfo  :   senderInfo,
            receiverInfo: receiverInfo,
            pickupDate  : pickupDate,
            pickupTime  : pickupTime,
        })
        await newOrder.save();
        return res.status(201).json({ "msg": "Order confirmed!" });
    }
    catch {
        return res.status(500).json({ "msg": "Order confirmation API goes something wrong/unknown" });
    }
});

export default router;
