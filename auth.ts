import * as express from "express";
import * as jwt from "jsonwebtoken";
import User, { UserRole } from "./mongoose_schemas/user";
import * as bcrypt from "bcryptjs";

const router = express.Router();
router.post("/register", async (req: express.Request, res: express.Response) => {
    const { username, password, role } = req.body;
    if (!Object.values(UserRole).includes(role)) {
        return res.status(400).send("Role not found")
    }
    try {
        const newUser = new User({ username, password, role });
        await newUser.save();
        res.status(201).send("User registered successfully");
    }
    catch
    {
        res.status(500).send("Error registering user");
    }
});
router.post("/login", async (req: express.Request, res: express.Response) => {
    const { username, password } = req.body;
    try {
        const user = await User.findOne({ username }).exec();
        if (!user) {
            return res.status(401).send("User not found");
        }
        const isPasswordMatch = await user.ComparePassword(await bcrypt.hash(password, 10));
        if (!isPasswordMatch) {
            return res.status(401).send("Invalid password");
        }
        const payload = { sub: user._id };
        const token = jwt.sign(payload, process.env.JWT_SECRET_KEY, { expiresIn: "30m" });
        res.json({ token });
    }
    catch (err) {
        res.status(500).send("Error logging in");
    }
});
export default router;