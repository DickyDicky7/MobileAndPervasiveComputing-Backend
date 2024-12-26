(async () => { const staffs = await db.staffs.find(); for (const staff of staffs) {
 await db.staffs.findOneAndUpdate(
      { _id : staff._id  },
      { $set: { __v: 0 } },
   );
}
})();