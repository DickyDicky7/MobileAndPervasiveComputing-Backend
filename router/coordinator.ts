import * as express from "express"                        ;
import        axios from              "axios"             ;
import  Coordinator from "../mongoose_schemas/coordinator";
import  mongoose    from    "mongoose"                    ;

const router = express.Router();


router.get("/coordinator/byCoordinatorUserId", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const { coordinatorUserId } = req.query;
        if    (!coordinatorUserId )
            return res.status(400).json({ message: "Operation failure: coordinatorUserId is required",                                                                                                                  });
        else
            return res.status(200).json({ message: "Operation success:                              ", data: await Coordinator.findOne({ coordinatorUserId: new mongoose.Types.ObjectId(coordinatorUserId as string) }) });
    } catch (err) {
        next(err);
    }
})


router.get("/coordinator/byCoordinator_HubId", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const { coordinator_HubId } = req.query;
        if    (!coordinator_HubId )
            return res.status(400).json({ message: "Operation failure: coordinator_HubId is required",                                                                                                                  });
        else
            return res.status(200).json({ message: "Operation success:                              ", data: await Coordinator.findOne({ coordinator_HubId: new mongoose.Types.ObjectId(coordinator_HubId as string) }) });
    } catch (err) {
        next(err);
    }
})


router.post("/coordinator/insert", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const { coordinatorUserId, coordinator_HubId } = req.body;
        if (!coordinatorUserId)
            return res.status(400).json({ message: "Operation failure: coordinatorUserId is required",                      });
        if (!coordinator_HubId)
            return res.status(400).json({ message: "Operation failure: coordinator_HubId is required",                      });
        const newCoordinator = new Coordinator({
            coordinatorUserId: new mongoose.Types.ObjectId(coordinatorUserId),
            coordinator_HubId: new mongoose.Types.ObjectId(coordinator_HubId),
        })
        await newCoordinator.save();
            return res.status(200).json({ message: "Operation success:                              ", data: newCoordinator });
    } catch (err) {
        next(err);
    }
})


router.put("/coordinator/update/byCoordinatorUserId", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const {
             coordinatorUserId,
             coordinator_HubId,  } = req.body;
        if (!coordinatorUserId)
            return res.status(400).json({ message: "Operation failure: coordinatorUserId is required",                           });
        if (!coordinator_HubId)
            return res.status(400).json({ message: "Operation failure: coordinator_HubId is required",                           });
        const toUpdateCoordinator = await Coordinator.findOne({ coordinatorUserId: new mongoose.Types.ObjectId(coordinatorUserId as string) });
              toUpdateCoordinator                    .          coordinator_HubId= new mongoose.Types.ObjectId(coordinator_HubId as string   );
        await toUpdateCoordinator .save();
            return res.status(200).json({ message: "Operation success:                              ", data: toUpdateCoordinator });
    } catch (err) {
        next(err);
    }
})


router.put("/coordinator/update/byCoordinator_HubId", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const {
             coordinatorUserId,
             coordinator_HubId,  } = req.body;
        if (!coordinatorUserId)
            return res.status(400).json({ message: "Operation failure: coordinatorUserId is required",                           });
        if (!coordinator_HubId)
            return res.status(400).json({ message: "Operation failure: coordinator_HubId is required",                           });
        const toUpdateCoordinator = await Coordinator.findOne({ coordinator_HubId: new mongoose.Types.ObjectId(coordinator_HubId as string) });
              toUpdateCoordinator                    .          coordinatorUserId= new mongoose.Types.ObjectId(coordinatorUserId as string   );

        await toUpdateCoordinator .save();
            return res.status(200).json({ message: "Operation success:                              ", data: toUpdateCoordinator });
    } catch (err) {
        next(err);
    }
})


router.delete("/coordinator/update/byCoordinatorUserId", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const { coordinatorUserId } = req.query;
        if    (!coordinatorUserId )
            return res.status(400).json({ message: "Operation failure: coordinatorUserId is required",                                                                                                                    });
        else
            return res.status(200).json({ message: "Operation success:                              ", data: await Coordinator.deleteOne({ coordinatorUserId: new mongoose.Types.ObjectId(coordinatorUserId as string) }) });
    } catch (err) {
        next(err);
    }
})


router.delete("/coordinator/update/byCoordinator_HubId", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const { coordinator_HubId } = req.query;
        if    (!coordinator_HubId )
            return res.status(400).json({ message: "Operation failure: coordinator_HubId is required",                                                                                                                    });
        else
            return res.status(200).json({ message: "Operation success:                              ", data: await Coordinator.deleteOne({ coordinator_HubId: new mongoose.Types.ObjectId(coordinator_HubId as string) }) });
    } catch (err) {
        next(err);
    }
})


export default router;
