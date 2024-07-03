import * as express from "express"     ;
import * as jwt     from "jsonwebtoken"; import User, { UserRole, TUser } from "../mongoose_schemas/user";
import * as  bcrypt from     "bcryptjs";

const router = express.Router();

router.post("/sign-up", async (req: express.Request, res: express.Response, next: express.RequestHandler) => {
    const { username, password, role } = req.body;
    if (!Object.values(UserRole).includes(role)) {
        return res.status(400).json({"msg": "Role not found"});
    }
    try {
        const newUser = new User(
          { username, password, role });
        await newUser.save();
        return res.status(201).json({"msg": "Sign up okkkkk"});
    }
    catch
    {
        return res.status(500).json({"msg": "Sign up API goes something wrong/unknown"});
    }
});

router.post("/sign-in", async (req: express.Request, res: express.Response, next: express.RequestHandler) => {
    const { username, password } = req.body;
    try {
        const user: TUser = await User.findOne({ username: username });
        if  (!user)            {
            return res.status(401).json({"msg": "Username not found"});
        }
        // console.log(user.password);
        // console.log(     password);
        const isPasswordMatch = await user.ComparePassword(password);
        if  (!isPasswordMatch) {
            return res.status(401).json({"msg": "Password not match"});
        }
        const payLoad = { sub: user._id };
        const  token  =   jwt.sign(payLoad, process.env.JWT_SECRET_KEY, { expiresIn: "24h" });
        res.json({ "data": token });
    }
    catch (err) {
        res.status(500).json({"msg": "Sign in API goes something wrong/unknown"});
    }
});

export default router;