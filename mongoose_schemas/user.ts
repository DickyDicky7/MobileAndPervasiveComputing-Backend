import mongoose from "mongoose";

const user = new mongoose.Schema({
    username: { type: String },
    password: { type: String },
});

const User = mongoose.model("User", user);

export default User;