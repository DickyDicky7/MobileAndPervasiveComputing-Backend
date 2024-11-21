const swaggerAutogen = require("swagger-autogen")();

const doc = { info: { title: "Mobile And Pervasive Computing API", description: "API này của node express nha ô. API này được map từ python server của ô sang node express - handle thêm một số thứ nhỏ và hỗ trợ cho input của mỗi address bên python server của ô." }, host: "https://waseminarcnpm2.azurewebsites.net/" };

const outputFile =   "./swagger-output.json";
const routes     = [ "./index.ts",
                                "./router/a.i.ts",
                                                "./router/assign.ts",
                                                                   "./router/auth.ts",
                                                                                    "./router/delivery.ts",
                                                                                                         "./router/hub.ts",
                                                                                                                         "./router/order.ts",
                                                                                                                                           "./router/staff.ts",
                                                                                                                                                             "redisClient.ts",
                                                                                                                                                             "mongoClient.ts",
                                                                                                                                                             "passportJwt.ts",
                                                                                                                                                                            "./mongoose_schemas/hub.ts",
                                                                                                                                                                                                      "./mongoose_schemas/order.ts",
                                                                                                                                                                                                                                  "./mongoose_schemas/staff.ts",
                                                                                                                                                                                                                                                              "./mongoose_schemas/user.ts", ];

//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

swaggerAutogen(outputFile, routes, doc);

