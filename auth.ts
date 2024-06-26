import * as express from 'express';
import jwt from 'jsonwebtoken';
import User from './mongoose_schemas/user';

const router = express.Router();
router.post('/register', async(req: express.Request, res: express.Response) => {
    const {username, password} = req.body;
    try
    {
        const newUser = new User({ username, password });
        await newUser.save();
        res.status(201).send('User registered successfully');
    }
    catch
    {
        res.status(500).send('Error registering user');
    }
});
router.post('/login', async(req: express.Request, res: express.Response) => {
    const {username, password} = req.body;
    try
    {
        const user = await User.findOne({username}).exec();
        if (!user)
        {
            return res.status(401).send('User not found');
        }
        const isPasswordMatch = await user.ComparePassword(password);
        if (!isPasswordMatch)
        {
            return res.status(401).send('Invalid password');
        }
        const payload = { sub: user._id };
        const token = jwt.sign(payload, 'laughOutLoud', { expiresIn: '1h' });
        res.json({ token });
    } 
    catch (err)
    {
        res.status(500).send('Error logging in');
    }
});
export default router;