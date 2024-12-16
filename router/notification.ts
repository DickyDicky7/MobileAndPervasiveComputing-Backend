import * as express from "express";
import axios    from "axios";
import mongoose from "mongoose";
import Notification from "../mongoose_schemas/notification";

const router = express.Router();

router.post('/notification', async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const {
            orderId,
            senderId,
            receiverId,
            date,
            about,
            status,
        } = req.body;
        try {
            const newNotification = new Notification({
                orderId: orderId, 
                senderId: senderId, 
                receiverId: receiverId, 
                date: date, 
                about: about, 
                status: status
            });
            await newNotification.save();
            return res.status(200).json({
                "message": "Notification created successfully"
            })
        }
        catch(error){
            return res.status(500).json({
                "message": "Failed to create notification",
                "error": error,
            })
        }
    }
    catch(error) {
        next(error);
    }
})
router.get('notifications/orderId', async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try{
        const {orderId} = req.body;
        try{
            const notifications = await Notification.find({orderId: orderId});
            if (!notifications || notifications.length === 0){
                return res.status(404).json({
                    "message": `No notifications are found with orderId ${orderId}.`
                })
            }
            return res.status(200).json({
                "message": "Notifcations found!",
                "data": notifications,
            })
        }
        catch (error){
            return res.status(500).json({
                "message": "Failed to get notifications",
                "error": error,
            })
        }
    }
    catch(error){
        next(error);
    }
})
router.get('notifications/senderId', async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try{
        const {senderId} = req.body;
        try{
            const notifications = await Notification.find({senderId: senderId});
            if (!notifications || notifications.length === 0){
                return res.status(404).json({
                    "message": `No notifications are found with senderId ${senderId}.`
                })
            }
            return res.status(200).json({
                "message": "Notifcations found!",
                "data": notifications,
            })
        }
        catch (error){
            return res.status(500).json({
                "message": "Failed to get notifications",
                "error": error,
            })
        }
    }
    catch(error){
        next(error);
    }
})
router.get('notifications/receiverId', async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try{
        const {receiverId} = req.body;
        try{
            const notifications = await Notification.find({receiverId: receiverId});
            if (!notifications || notifications.length === 0){
                return res.status(404).json({
                    "message": `No notifications are found with senderId ${receiverId}.`
                })
            }
            return res.status(200).json({
                "message": "Notifcations found!",
                "data": notifications,
            })
        }
        catch (error){
            return res.status(500).json({
                "message": "Failed to get notifications",
                "error": error,
            })
        }
    }
    catch(error){
        next(error);
    }
})

export default router;