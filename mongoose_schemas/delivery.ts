import mongoose from "mongoose";
import * as express from "express";

export interface IDelivery extends mongoose.Document {
    staffId: mongoose.Types.ObjectId,
    orderId: mongoose.Types.ObjectId,
    hubId: mongoose.Types.ObjectId,
    date: string,
    deliverTimes: number,
    status: string,
}

const delivery: mongoose.Schema<IDelivery> = new mongoose.Schema({
    staffId: { type: mongoose.Schema.Types.ObjectId, required: true },
    orderId: { type: mongoose.Schema.Types.ObjectId, required: true },
    hubId:   { type: mongoose.Schema.Types.ObjectId, required: true },
    date:    { type: String, required: true, match: /^\d{4}-\d{2}-\d{2}$/ },
    deliverTimes: { type: Number, required: true },
    status:  { type: String, required: true },
});

const Delivery = mongoose.model("Delivery", delivery);

export default Delivery;