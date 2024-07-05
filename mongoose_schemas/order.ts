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
    userId     : string,
    name       : string,
    address    : string,
    phoneNumber: number,
}
interface IReceiverInfo {
    userId     : string,
    name       : string,
    address    : string,
    phoneNumber: number,
}
export interface IOrder extends mongoose.Document {
    shipmentType: ShipmentType,
    deliveryType: DeliveryType,
      senderInfo:   ISenderInfo,
    receiverInfo: IReceiverInfo,
    weight      : number,
    status      : string,
    packageSize : number,
    pickupDate  : string,
    pickupTime  : string,
    value       : number,
    hubId       :  mongoose.Types.ObjectId,
    deliveryAddress: string,
            message: string,
    inProgress: boolean,
}
//schema
const   senderInfo: mongoose.Schema<  ISenderInfo> = new mongoose.Schema({
    userId     : { type: String, required: true },
    name       : { type: String, required: true },
    address    : { type: String, required: true },
    phoneNumber: { type: Number, required: true },
});
const receiverInfo: mongoose.Schema<IReceiverInfo> = new mongoose.Schema({
    userId     : { type: String, required: true },
    name       : { type: String, required: true },
    address    : { type: String, required: true },
    phoneNumber: { type: Number, required: true },
});
const order: mongoose.Schema<IOrder> = new mongoose.Schema({
    shipmentType: { type: String, enum: ShipmentType, required: true },
    deliveryType: { type: String, enum: DeliveryType, required: true },
      senderInfo: { type:   senderInfo, required: true },
    receiverInfo: { type: receiverInfo, required: true },
    weight      : { type: Number, required: true },
    status      : { type: String, required: true },
    packageSize : { type: Number, required: true },
    pickupDate  : { type: String, required: true, match: /^\d{4}-\d{2}-\d{2}$/ },
    pickupTime  : { type: String, required: true, match: /^([01]\d|2[0-3]):([0-5]\d)$/ },
    value       : { type: Number, required: true },
    hubId       : { type: mongoose.Schema.Types.ObjectId, required: true },
    deliveryAddress: { type: String, required: true },
            message: { type: String, required: true },
    inProgress: { type: Boolean, required: true },
});

export const getOrdersByUserIdAndStatus: express.Handler = async (
    req: express.Request, res: express.Response, next: express.NextFunction
) => {
    const { userId, status } = req.body;
    try{
        if (!userId){
            return res.status(400).json({"msg": "userId is required"});
        }
        const orders = await Order.find({
            $or: [{ "senderInfo.userId": userId }, { "receiverInfo.userId": userId }],
            status: status
        });
        return res.status(200).json({"orders": orders});
    }
    catch(error){
        return res.status(500).json({ "msg": "Something went wrong"});
    }
}

const Order = mongoose.model("Order", order);

export default Order;