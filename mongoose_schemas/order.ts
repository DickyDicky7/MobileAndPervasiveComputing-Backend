import mongoose from "mongoose";
import * as express from "express";

//enum
export enum ShipmentType {
    Document = "Document",
     Package =  "Package",
    Parcel   = "Parcel"  ,
}
export enum DeliveryType {
    Standard = "Standard",
    Express  = "Express" ,
    SameDay  = "SameDay" ,
}
//component interface
interface   ISenderInfo {
    userId     : mongoose.Types.ObjectId,
    name       : string,
    address    : string,
    phoneNumber: string,
}
interface IReceiverInfo {
    userId     : mongoose.Types.ObjectId,
    name       : string,
    address    : string,
    phoneNumber: string,
}
interface IDeliveryInfo {
    shipmentType: ShipmentType,
    deliveryType: DeliveryType,
         status : string,
    packageSize : number,
    pickupDate  : string,
    pickupTime  : string,
    value       : number,
}
export interface IOrder extends mongoose.Document {
      senderInfo:   ISenderInfo,
    receiverInfo: IReceiverInfo,
    deliveryInfo: IDeliveryInfo,
    hubId       :  mongoose.Types.ObjectId,
    message  : string,
    podTxt   : string,
    podImg   : string,
    payStatus: string, // pending | success | cancel
    payWith  : string, // momo    | cash    | wallet
}
//schema
const   senderInfo: mongoose.Schema<  ISenderInfo> = new mongoose.Schema({
    userId     : { type: mongoose.Schema.Types.ObjectId, required: true },
    name       : { type: String, required: true },
    address    : { type: String, required: true },
    phoneNumber: { type: String, required: true },
});
const receiverInfo: mongoose.Schema<IReceiverInfo> = new mongoose.Schema({
    userId     : { type: mongoose.Schema.Types.ObjectId, required: true },
    name       : { type: String, required: true },
    address    : { type: String, required: true },
    phoneNumber: { type: String, required: true },
});
const deliveryInfo: mongoose.Schema<IDeliveryInfo> = new mongoose.Schema({
    shipmentType: { type: String, enum: ShipmentType, required: true },
    deliveryType: { type: String, enum: DeliveryType, required: true },
    status      : { type: String, required: true },
    packageSize : { type: Number, required: true },
    pickupDate  : { type: String, required: true, match: /^\d{4}-\d{2}-\d{2}$/ },
    pickupTime  : { type: String, required: true, match: /^([01]\d|2[0-3]):([0-5]\d)$/ },
    value       : { type: Number, required: true },
});
const order: mongoose.Schema<IOrder> = new mongoose.Schema({
    
      senderInfo: { type:   senderInfo, required: true },
    receiverInfo: { type: receiverInfo, required: true },
    deliveryInfo: { type: deliveryInfo, required: true },
    hubId:        { type: mongoose.Schema.Types.ObjectId, required: true },
    message  : { type: String, required: true  },
    podTxt   : { type: String, required: false },
    podImg   : { type: String, required: false },
    payStatus: { type: String, required: true  }, // pending | success | cancel
    payWith  : { type: String, required: true  }, // momo    | cash    | wallet
});

export const getOrdersByUserIdAndStatus: express.Handler = async (
    req: express.Request, res: express.Response, next: express.NextFunction
) => {
    const { userId, status } = req.body;
    try {
        if (!userId){
            return res.status(400).json({ "msg": "userId is required" });
        }
        const orders = await Order.find({
            $or: [ { "senderInfo.userId": new mongoose.Types.ObjectId(userId) }, { "receiverInfo.userId": new mongoose.Types.ObjectId(userId) } ],
            "deliveryInfo.status": status
        });
        return res.status(200).json({ "orders": orders });
    }
    catch (error) {
        return res.status(500).json({ "msg": "Something went wrong" });
    }
}
export const getOrdersByUserIdAndType: express.Handler = async (
    req: express.Request, res: express.Response, next: express.NextFunction
) => {
    const { userId, type } = req.body;
    try {
        if (!userId) {
            return res.status(400).json({ "msg": "userId is required" });
        }
        var orders;
        if (type === "send") {
            orders = await Order.find({   "senderInfo.userId": new mongoose.Types.ObjectId(userId), });
        }
        if (type === "receive"){
            orders = await Order.find({ "receiverInfo.userId": new mongoose.Types.ObjectId(userId), });
        }
        return res.status(200).json({ "orders": orders });
    }
    catch (error) {
        return res.status(500).json({ "msg": "Something went wrong" });
    }
}

const Order = mongoose.model("Order", order);

export default Order;