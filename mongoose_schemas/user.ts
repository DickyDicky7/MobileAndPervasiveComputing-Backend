import mongoose from "mongoose";
import * as bcrypt from 'bcryptjs';

export enum UserRole{
    Sender = 'sender',
    Receiver = 'receiver',
    Shipper = 'shipper',
    Coordinator = 'coordinator'
}

export interface IUser extends mongoose.Document {
    username: string;
    password: string;
    email: string;
    role: UserRole;
    ComparePassword(password: string): Promise<boolean>;
  }

const user: mongoose.Schema<IUser> = new mongoose.Schema({
    username: { type: String, required: true, unique: true },
    password: { type: String, required: true },
    role: { type: String, enum: UserRole, required: true}, 
});

user.pre<IUser>('save', async function(next){
    if (this.isModified('password') || this.isNew)
    {
        this.password = await bcrypt.hash(this.password, 10);
    }
    next();
});

user.methods.ComparePassword = function(password: string): boolean
{
    return password == this.password;
};

const User = mongoose.model("User", user);

export default User;