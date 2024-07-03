import mongoose from "mongoose";
import * as express from "express";

export interface IHub extends mongoose.Document {
    name    : string,
    district: string,
}

const hub: mongoose.Schema<IHub> = new mongoose.Schema({
    name    : { type: String, required: true },
    district: { type: String, required: true },
});

const Hub = mongoose.model("Hub", hub);

export default Hub;