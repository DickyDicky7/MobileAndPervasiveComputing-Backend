import mongoose from "mongoose"; import * as express from "express"; import * as bcrypt from "bcryptjs";

export enum UserRole {
      Sender =   "sender",
    Receiver = "receiver",
    Shipper  = "shipper",
    Coordinator = "coordinator",
}

export interface IUser extends mongoose.Document {
    username: string;
    password: string;
    role: UserRole;
    ComparePassword(password: string): Promise<boolean>;
}

const user: mongoose.Schema<IUser> = new mongoose.Schema({
    username: { type: String, required: true, index: true, unique: true },
    password: { type: String, required: true,                           },
    role: { type: String, enum: UserRole,  required: true               },
});

user.pre<IUser>("save", async function (next) {
    if (this.isModified("password")
    ||  this.isNew) {
        this.password = await bcrypt.hash(this.password, 10);
    }
    next();
});

user.methods.ComparePassword =function (password: string): Promise<boolean> {
    return bcrypt.compare(password,this.password);
};

export const ensureUserExists: express.RequestHandler = async(req: express.Request, res: express.Response, next: express.NextFunction) => {
    const roles = Object.values(UserRole);
    const promises = (Array.from({length: 10}, (_, index) => index + 1)).map(async (index) => {
        for (var role of roles) {
            const newUsername = `${role.slice(0,2)}${index}` /* `${role}_username_${index}` */;
            const newPassword = `${role.slice(0,2)}${index}` /* `${role}_password_${index}` */;
            if (!(await User.exists({ username: newUsername }))) {
                const newUser = new User({
                    username: newUsername,
                    password: newPassword,
                    role: role
                })
                await newUser.save();
                console.log(`${newUser.username} | ${newUser.password} | ${newUser._id}`);
            }
        }
    });
    await Promise.all(promises);
    next();
}
export const getUserIdByUsername: express.RequestHandler = async(req: express.Request, res: express.Response, next: express.NextFunction) => {
    const { username } = req.body;
    try{
        if (!username){
            return res.status(400).json({"msg": "username is required"});
        }
        const user = await User.findOne({ username: username });
        if (user){
            return res.status(200).json({"userId": user._id});
        }
        else{
            return res.status(404).json({"msg": "User not found"});
        }
    }
    catch(error){
        return res.status(500).json({ "msg": "Something went wrong"});
    }
}

const User = mongoose.model("User", user);

export default User;

export
type          TUser = mongoose.Document<unknown, {}, IUser> & IUser & Required<{
    _id: unknown;
}>;
