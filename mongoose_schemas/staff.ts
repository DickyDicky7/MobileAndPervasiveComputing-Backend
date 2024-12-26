import     mongoose from "mongoose"        ;
import * as express from          "express";

export interface IStaff extends mongoose.Document {
    name              : string,
    age               : number,
    gender            : string,
    weight            : number,
    motorcycleCapacity: number,
     hubId: mongoose.Types.ObjectId,
    userId: mongoose.Types.ObjectId,
}

const staff: mongoose.Schema<IStaff> = new mongoose.Schema({
    name              : { type: String, required: true },
    age               : { type: Number, required: true },
    gender            : { type: String, required: true },
    weight            : { type: Number, required: true },
    motorcycleCapacity: { type: Number, required: true },
     hubId: { type: mongoose.Schema.Types.ObjectId, required: true },
    userId: { type: mongoose.Schema.Types.ObjectId, required: true },
});

const Staff = mongoose.model("Staff", staff);

export default Staff;
