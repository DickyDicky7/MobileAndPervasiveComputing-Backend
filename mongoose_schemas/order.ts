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
    name       : string,
    address    : string,
    phoneNumber: number,
}
interface IReceiverInfo {
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
    pickupDate  : Date  ,
    pickupTime  : string,
    value       : number,
    hubId       :  mongoose.Types.ObjectId,
    deliveryAddress: string,
            message: string,
    inProgress: boolean,
}
//schema
const   senderInfo: mongoose.Schema<  ISenderInfo> = new mongoose.Schema({
    name       : { type: String, required: true },
    address    : { type: String, required: true },
    phoneNumber: { type: Number, required: true },
});
const receiverInfo: mongoose.Schema<IReceiverInfo> = new mongoose.Schema({
    name       : { type: String, required: true },
    address    : { type: String, required: true },
    phoneNumber: { type: Number, required: true },
});
const order: mongoose.Schema<IOrder> = new mongoose.Schema({
    shipmentType: { type: String, enum: ShipmentType, required: true },
    deliveryType: { type: String, enum: DeliveryType, required: true },
    senderInfo  : { type:   senderInfo, required: true },
    receiverInfo: { type: receiverInfo                 },
    weight      : { type: Number, required: true },
    status      : { type: String, required: true },
    packageSize : { type: Number, required: true },
    pickupDate  : { type: Date  , required: true },
    pickupTime  : { type: String, required: true, match: /^([01]\d|2[0-3]):([0-5]\d)$/ },
    value       : { type: Number, required: true },
    hubId       : { type: mongoose.Schema.Types.ObjectId, required: true },
    deliveryAddress: { type: String, required: true },
            message: { type: String, required: true },
    inProgress: { type: Boolean, required: true },
});

const Order = mongoose.model("Order", order);

export default Order;