import     mongoose from "mongoose"        ;
import * as express from          "express";

export interface ICoordinator extends mongoose.Document {
    coordinator_HubId: mongoose.Types.ObjectId,
    coordinatorUserId: mongoose.Types.ObjectId,
}

const coordinator: mongoose.Schema<ICoordinator> = new mongoose.Schema({
    coordinator_HubId: { type: mongoose.Schema.Types.ObjectId, required: true },
    coordinatorUserId: { type: mongoose.Schema.Types.ObjectId, required: true },
});

const Coordinator= mongoose.model( "Coordinator" , coordinator );

export default Coordinator;
