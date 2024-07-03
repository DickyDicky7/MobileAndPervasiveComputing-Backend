import User from "./mongoose_schemas/user";

import          passport = require("passport");
const        JwtStrategy = require("passport-jwt"). Strategy ;
const ExtractJwt         = require("passport-jwt").ExtractJwt;

const options = {
    jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
       secretOrKey:    process.env.JWT_SECRET_KEY           ,
};

passport.use(new JwtStrategy(options, async (jwtPayload, done) => {
    try {
        const user = await User.findById(jwtPayload.sub);
        if   (user) {
            return done(null, user );
        }
        else        {
            return done(null, false);
        }
    }
    catch (err) {
        return done(err, false);
    }
}));

export default passport;