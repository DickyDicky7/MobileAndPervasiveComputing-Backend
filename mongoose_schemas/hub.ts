import mongoose from "mongoose";
import * as express from "express";

export interface IHub extends mongoose.Document {
    name   : string,
    address: string,
}

const hub: mongoose.Schema<IHub> = new mongoose.Schema({
    name   : { type: String, required: true },
    address: { type: String, required: true },
});

const Hub = mongoose.model("Hub", hub);

export default Hub;