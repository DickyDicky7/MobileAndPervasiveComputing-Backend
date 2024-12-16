import     mongoose from "mongoose"        ;
import * as express from          "express";

export enum DeliveryStatus {
    Pending    =
   "pending"   ,
    InProgress =
   "inProgress",
    Success    =
   "success"   ,
    Failed     =
   "failed"    , 
    Canceled   =
   "canceled"  ,
}

export enum PaymentStatus {
    Pending  =
   "pending" , 
    Success  =
   "success" ,
    Canceled =
   "canceled",
}

export enum About {
    Payment  =
   "payment" ,
    Delivery =
   "delivery",
}

export interface INotification extends mongoose.Document{
       orderId: mongoose.Types.ObjectId,
      senderId: mongoose.Types.ObjectId,
    receiverId: mongoose.Types.ObjectId,
    date  : string,
     about:              About         ,
    status: DeliveryStatus | PaymentStatus;
}

const notification: mongoose.Schema<INotification> = new mongoose.Schema({
       orderId: { type: mongoose.Schema.Types.ObjectId, required: true, },
      senderId: { type: mongoose.Schema.Types.ObjectId, required: true, },
    receiverId: { type: mongoose.Schema.Types.ObjectId, required: true, },
    date  : { type: String,             required: true, match: /^\d{4}-\d{2}-\d{2}$/ },
     about: { type: String, enum: About,required: true,                              },
    status: { type: String,             required: true,
        validate : {
        validator: function (value: string) {
                if (this.about === About.Delivery) {
                    return Object.values(DeliveryStatus).includes(value as DeliveryStatus);
                }
                else
                if (this.about === About. Payment) {
                    return Object.values( PaymentStatus).includes(value as  PaymentStatus);
                }
                return false;
            },
            message: (props) => `"status": ${props.value} is not invalid for the provided "about"`,
        }
    }
})

const          Notification = mongoose.model(
              "Notification"                 ,
               notification                 );

export default Notification;