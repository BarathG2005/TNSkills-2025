import { headers } from "next/headers";
import Image from "next/image";
import { useEffect, useState } from "react";
export default function Home() {
  const [data,setData] = useState();
  useEffect(()=>{
    const fetch =async()=> {
      const res = await fetch("https://localhost:8080/available",{
        methods:"GET",
        headers:{
          "content-Type":"application/json",
        }
      })
    const data = await res.json();
    return data
  }
    setData(fetch())
  
},[])
  return (
    <div> </div>
  )
}