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
interface ISenderInfo {
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
    senderInfo  :   ISenderInfo,
    receiverInfo: IReceiverInfo,
    packageSize : number,
    pickupDate  : Date  ,
    pickupTime  : string,
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
    packageSize : { type: Number, required: true },
    pickupDate  : { type: Date  , required: true },
    pickupTime  : { type: String, required: true, match: /^([01]\d|2[0-3]):([0-5]\d)$/ },
    message: {type: String},
    inProgress: {type: Boolean},
});

const Order = mongoose.model("Order", order);

export default Order;