const mysql = require("mysql");

const pool = mysql.createPool({
  host: "localhost",
  database: "neural_art",
  user: "root",
  password: "",
});

const executeQuery = (q, bind) => {
  return new Promise((resolve, reject) => {
    pool.getConnection((err, conn) => {
      if (err) {
        reject(err);
      } else {
        conn.query(q, bind, (err, results) => {
          if (err) {
            reject(err);
          } else {
            resolve(results);
          }
          conn.release();
        });
      }
    });
  });
};

module.exports = executeQuery;
