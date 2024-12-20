import * as express    from
           "express"               ;
import axios                       ,
     { AxiosResponse } from "axios";
import mongoose from
      "mongoose"                   ;



       const router = express
            .Router();


            
export const OneSignalSendPushNotificationTo = async (userId: string | mongoose.Types.ObjectId, contentEn: string, headingEn: string, subtitleEn: string): Promise<AxiosResponse<any, any>> => {
    const result = await axios.post("https://api.onesignal.com/notifications/"
    ,
    {
        app_id: "9aea25d1-efcd-4578-9fad-ffeb401ae64e"
    ,   contents: {
            en: contentEn
         ,
        },
        headings: {
            en: headingEn
         ,
        },
        subtitle: {
            en: subtitleEn
         ,
        },
         target_channel: "push",
        include_aliases: {
            external_id: [
                userId instanceof String ?
                userId : userId.toString()
             ,
            ],
        },
    }
    ,
    {
        headers: {
            //---------------------------------------------------//
            Authorization: `Key ${process.env.ONE_SIGNAL_AUTH_KEY}`
            //---------------------------------------------------//
            ,
        }
        ,
    });
    return result;
}



router.post("/one-signal/send-push-notification", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const { userId,   contentEn,   headingEn,   subtitleEn } = req.body;
        if    ( userId && contentEn && headingEn && subtitleEn ) {
//          ----------------------------------------------------
            const result = await OneSignalSendPushNotificationTo
//          ----------------------------------------------------
              ( userId,   contentEn,   headingEn,   subtitleEn ) ;
            res.status(200).json(result.data);
//          res.status(200).json(result     );
        } else {
            res.status(400).json({ "msg": "Invalid request | reason: userId or contentEn or headingEn or subtitleEn is misssing" });
        }
    } catch (err) {
        next(err) ;
    }
});;



export default router;


