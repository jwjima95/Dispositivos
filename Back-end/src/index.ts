import express, {Express} from "express";
import cors from "cors";

const app :Express = express();
app.use(express.json());

const PORT = 3000;

app.use(cors());

app.get("/ping", (req,res)=> {
    console.log("alguien ha dado ping!!!!");
    res.setHeader("Contet-Type", "appication/json");
    res.send("pong");
})

app.get("/hola/:nombre/:apellido", (req,res)=> {
    res.setHeader("Contet-Type", "appication/json");
    const nombre = req.params.nombre;
    const apellido = req.params.apellido;
    console.log("Alguien ah ingresado sus nombres!!");
    res.send({nombre: nombre, apellido: apellido});
})

app.listen(PORT, () :void => {
    console.log("server running in port" + PORT)
})