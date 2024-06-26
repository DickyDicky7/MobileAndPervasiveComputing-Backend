import mongoose from "mongoose";

export interface IUser extends mongoose.Document {
    username: string;
    password: string;
    email: string;
    ComparePassword(password: string): Promise<boolean>;
  }

const user: mongoose.Schema<IUser> = new mongoose.Schema({
    username: { type: String },
    password: { type: String },
    
});

user.methods.ComparePassword = function(password: string): boolean
{
    return password == this.password;
};

const User = mongoose.model("User", user);

export default User;