import { useForm } from "react-hook-form";
import { useState, useEffect } from "react";

export default function Form() {
  const { register, handleSubmit } = useForm();
  const [options, setOptions] = useState({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setOptions({
      Brand: ['Apple','Lenovo','Asus','HP','DELL','Acer','MSI'],
      Processor_Brand: ['Intel','AMD','Apple','Qualcomm'],
      RAM: ['4 GB','8 GB','16 GB','32 GB'],
      SSD_Capacity: ['128 GB','256 GB','512 GB','1 TB']
    });
  }, []);

  const onSubmit = async (data) => {
    setLoading(true);

    const payload = {
      Brand: data.Brand,
      "Processor Brand": data.Processor_Brand,
      RAM: data.RAM,
      "SSD Capacity": data.SSD_Capacity,
      "Screen Size": data.Screen_Size
    };

    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const result = await response.json();
      alert(`Predicted Laptop Price: ₹${result["Predicted Price"]}`);
    } catch (error) {
      alert("Prediction failed");
    }

    setLoading(false);
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2 style={styles.title}>💻 Laptop Price Predictor</h2>
        <p style={styles.subtitle}>Enter specs to estimate price</p>

        <form onSubmit={handleSubmit(onSubmit)}>

          <div style={styles.field}>
            <label>Brand</label>
            <select style={styles.input} {...register("Brand")}>
              {options.Brand?.map((b) => <option key={b}>{b}</option>)}
            </select>
          </div>

          <div style={styles.field}>
            <label>Processor Brand</label>
            <select style={styles.input} {...register("Processor_Brand")}>
              {options.Processor_Brand?.map((p) => <option key={p}>{p}</option>)}
            </select>
          </div>

          <div style={styles.field}>
            <label>RAM</label>
            <select style={styles.input} {...register("RAM")}>
              {options.RAM?.map((r) => <option key={r}>{r}</option>)}
            </select>
          </div>

          <div style={styles.field}>
            <label>SSD Capacity</label>
            <select style={styles.input} {...register("SSD_Capacity")}>
              {options.SSD_Capacity?.map((s) => <option key={s}>{s}</option>)}
            </select>
          </div>

          <div style={styles.field}>
            <label>Screen Size</label>
            <input 
              style={styles.input} 
              {...register("Screen_Size")} 
              placeholder="e.g. 15.6 Inch" 
            />
          </div>

          <button style={styles.button} type="submit" disabled={loading}>
            {loading ? "Predicting..." : "Predict Price"}
          </button>

        </form>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "linear-gradient(135deg, #1e1b4b, #6d28d9)",
    fontFamily: "sans-serif"
  },
  card: {
    background: "white",
    padding: "2rem",
    borderRadius: "12px",
    width: "350px",
    boxShadow: "0 10px 25px rgba(0,0,0,0.2)"
  },
  title: {
    textAlign: "center",
    marginBottom: "0.5rem",
    color: "#4c1d95"
  },
  subtitle: {
    textAlign: "center",
    marginBottom: "1.5rem",
    color: "#6b7280"
  },
  field: {
    marginBottom: "1rem",
    display: "flex",
    flexDirection: "column"
  },
  input: {
    padding: "0.5rem",
    borderRadius: "6px",
    border: "1px solid #d1d5db",
    marginTop: "0.3rem"
  },
  button: {
    width: "100%",
    padding: "0.6rem",
    background: "#7c3aed",
    color: "white",
    border: "none",
    borderRadius: "6px",
    fontWeight: "bold",
    cursor: "pointer",
    marginTop: "1rem"
  }
};