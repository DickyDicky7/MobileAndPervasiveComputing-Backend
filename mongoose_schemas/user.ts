import mongoose from "mongoose";
import * as bcrypt from "bcryptjs";
import { NextFunction } from "express";

export enum UserRole {
    Sender = "sender",
    Receiver = "receiver",
    Shipper = "shipper",
    Coordinator = "coordinator"
}

export interface IUser extends mongoose.Document {
    username: string;
    password: string;
    id: number;
    role: UserRole;
    ComparePassword(password: string): Promise<boolean>;
}

const user: mongoose.Schema<IUser> = new mongoose.Schema({
    username: { type: String, required: true },
    password: { type: String, required: true },
    id: { type: Number, required: true, unique: true },
    role: { type: String, enum: UserRole, required: true },
});

user.pre<IUser>("save", async function (next) {
    if (this.isModified("password") || this.isNew) {
        this.password = await bcrypt.hash(this.password, 10);
    }
    next();
});

user.methods.ComparePassword = function (password: string): boolean {
    return password == this.password;
};

export async function EnsureUserExists(req, res, next) {
    const roles = Object.values(UserRole);
    const promises = roles.map(async (role) => {
        for (let i = 0; i < 10; i++){
            const newUsername = `${role}_username_${i}`;
            const newPassword = `${role}_password_${i}`;
            const isUserExist = await User.findOne({newUsername}).exec();
            if (!isUserExist){
                const newUser = new User({
                    username: newUsername,
                    password: newPassword,
                    id: i,
                    role: role
                })
                await newUser.save();
            }
        }
    });
    await Promise.all(promises);
    next();
}

const User = mongoose.model("User", user);

export default User;