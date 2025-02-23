import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { motion, AnimatePresence } from "framer-motion";
import Laptop from "../images/laptop.png"
const styles = {
  container: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    minHeight: "100vh",
    background: "linear-gradient(45deg,rgb(50, 13, 83), black)",
    padding: "1rem",
    margin:"auto"
  },
  innercontainer:{
    display: "flex",
    width:"80vw",
    marginLeft:"300px"
  },
  formContainer: {
    width: "70%",
    
    backgroundColor: "white",
    borderRadius: "0.5rem",
    boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
    overflow: "hidden",
    backgroundColor: "#F3E8FF",
  },
  formContent: {
    padding: "1.5rem",
  },
  title: {
    fontSize: "1.5rem",
    fontWeight: "bold",
    textAlign: "center",
    color: "#6B46C1",
    marginBottom: "0.5rem",
  },
  subtitle: {
    textAlign: "center",
    color: "#7C3AED",
    marginBottom: "1.5rem",
  },
  stepTitle: {
    fontSize: "1.25rem",
    fontWeight: "600",
    marginBottom: "1rem",
    color: "#7C3AED",
    display: "flex",
    alignItems: "center",
  },
  input: {
    width: "60%",
    padding: "0.5rem 0.75rem",
    border: "1px solid #D1D5DB",
    borderRadius: "0.375rem",
    marginBottom: "1rem",
  },
  label: {
    display: "block",
    marginBottom: "0.5rem",
    fontSize: "0.875rem",
    fontWeight: "500",
    color: "#4B5563",
  },
  button: {
    backgroundColor: "#7C3AED",
    color: "white",
    fontWeight: "bold",
    padding: "0.5rem 1rem",
    borderRadius: "0.375rem",
    border: "none",
    cursor: "pointer",
    transition: "background-color 0.3s",
  },
  backButton: {
    backgroundColor: "white",
    color: "#7C3AED",
    border: "1px solid #7C3AED",
  },
  buttonContainer: {
    display: "flex",
    justifyContent: "space-between",
    marginTop: "1rem",
  },
  pre: {
    padding: "0.75rem",
    backgroundColor: "#F3E8FF",
    borderRadius: "0.375rem",
    fontSize: "0.875rem",
    color: "#4B5563",
    overflowX: "auto",
  },
  image:{
    position:"absolute",
    right:"270px",
    filter: "drop-shadow(0 0 5px white)",
  }
}
export default function Form() {
  const { register, handleSubmit, watch } = useForm();
  const [step, setStep] = useState(1);
  const [options, setOptions] = useState({});
  const [rotate, setRotate] = useState(false);

  useEffect(() => {
    setRotate(true); // Apply rotation on refresh
  }, []);

  useEffect(() => {
    const hardcodedData = {
      Brand: ['Apple', 'Lenovo', 'Primebook', 'Colorful', 'MSI', 'Asus', 'CHUWI',
       'Infinix', 'Ultimus', 'HP', 'DELL', 'Acer', 'Thomson', 'ZEBRONICS',
       'MICROSOFT', 'SAMSUNG', 'FUTOPIA', 'GIGABYTE', 'AXL', 'WINGS',
       'Avita', 'realme'],
      Type: ['Thin and Light Laptop', '2 in 1 Laptop', 'Gaming Laptop',
       'Business Laptop', 'Notebook', 'Laptop', 'Chromebook',
       'Dual Screen Laptop'],
      Operating_System: ['macOS Sequoia', 'Windows 11 Home', 'Prime OS', 'macOS Sonoma',
       'Windows 11 Pro', 'Chrome', 'Mac OS Big Sur', 'Mac OS Monterey',
       'Windows 10 Home', 'DOS', 'Ubuntu', 'Windows 10 Pro', 'Windows 10'],
       RAM:['16 GB', '8 GB', '4 GB', '12 GB', '36 GB', '32 GB', '24 GB',
       '48 GB', '18 GB'],
       Storage_Type:['SSD', 'eMMC', 'HDD', 'Hybrid'],
       Touchscreen:['Yes', 'No'],
       SSD_Capacity:['256 GB', '512 GB', 'nan', '1 TB', '128 GB'],
       Processor_Brand:['AMD', 'Intel', 'Qualcomm', 'Apple'],
       RAM_Type:['DDR4', 'DDR5', 'DDR3', 'DDR2'],
    };
    setOptions(hardcodedData);
  }, []);
  const nextStep = () => setStep((prev) => prev + 1);
  const prevStep = () => setStep((prev) => prev - 1);

  const onSubmit = async (data) => {
    try {
      console.log(data)
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      const result = await response.json();
      alert(`Predicted Laptop Price: ₹${result.predicted_price}`);
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to fetch prediction.");
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.innercontainer}>
      <div style={styles.formContainer}>
        <div style={styles.formContent}>
          <h2 style={styles.title}>Laptop Price Predictor</h2>
          <p style={styles.subtitle}>Fill in the details to predict the price</p>

          <AnimatePresence mode="wait">
            <motion.div key={step} initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              {step === 1 && (
                <div>
                  <h2 style={styles.stepTitle}>Basic Info</h2>
                  <label style={styles.label}>Brand</label>
                  <select style={styles.input} {...register("Brand")}>
                    {options.Brand?.map((item) => (
                      <option key={item} value={item}>
                        {item}
                      </option>
                    ))}
                  </select>

                  <label style={styles.label}>Type</label>
                  <select style={styles.input} {...register("Type")}>
                    {options.Type?.map((item) => (
                      <option key={item} value={item}>
                        {item}
                      </option>
                    ))}
                  </select>

                  <label style={styles.label}>Operating System</label>
                  <select style={styles.input} {...register("Operating_System")}>
                    {options.Operating_System?.map((item) => (
                      <option key={item} value={item}>
                        {item}
                      </option>
                    ))}
                  </select>
                     
                  <div style={styles.buttonContainer}>
                    <button style={styles.button} onClick={nextStep}>
                      Next
                    </button>
                  </div>
                </div>
              )}

              {step === 2 && (
                <div>
                  <h2 style={styles.stepTitle}>Display Details</h2>
                  <label style={styles.label}>Screen Size</label>
<input style={styles.input} {...register("Screen_Size")} placeholder="Enter screen size" />

<label style={styles.label}>Screen Resolution</label>
<input style={styles.input} {...register("Screen_Resolution")} placeholder="Enter screen Resolution" />

                  <div style={styles.buttonContainer}>
                    <button style={styles.button} onClick={prevStep}>
                      Back
                    </button>
                    <button style={styles.button} onClick={nextStep}>
                      Next
                    </button>
                  </div>
                </div>
              )}

              {step === 3 && (
                <div>
                  <h2 style={styles.stepTitle}>Processor & Memory</h2>
                  <label style={styles.label}>Processor Name</label>
<input style={styles.input} {...register("Processor Name")} placeholder="Enter Processor Name" />

                  <label style={styles.label}>RAM</label>
                  <select style={styles.input} {...register("RAM")}>
                    {options.RAM?.map((item) => (
                      <option key={item} value={item}>
                        {item}
                      </option>
                    ))}
                  </select>
                  <label style={styles.label}>RAM Type</label>
                  <select style={styles.input} {...register("RAM_Type")}>
                    {options.RAM_Type?.map((item) => (
                      <option key={item} value={item}>
                        {item}
                      </option>
                    ))}
                  </select>
                  <label style={styles.label}>Processor Brand</label>
                  <select style={styles.input} {...register("Processor_Brand")}>
                    {options.Processor_Brand?.map((item) => (
                      <option key={item} value={item}>
                        {item}
                      </option>
                    ))}
                  </select>

                  <label style={styles.label}>Storage Type</label>
                  <select style={styles.input} {...register("Storage_Type")}>
                    {options.Storage_Type?.map((item) => (
                      <option key={item} value={item}>
                        {item}
                      </option>
                    ))}
                  </select>

                  <div style={styles.buttonContainer}>
                    <button style={styles.button} onClick={prevStep}>
                      Back
                    </button>
                    <button style={styles.button} onClick={nextStep}>
                      Next
                    </button>
                  </div>
                </div>
              )}

              {step === 4 && (
                <div>
                  <h2 style={styles.stepTitle}>Additional Features</h2>
                  <label style={styles.label}>Touchscreen</label>
                  <select style={styles.input} {...register("Touchscreen")}>
                    <option value="Yes">Yes</option>
                    <option value="No">No</option>
                  </select>

                  <label style={styles.label}>SSD Capacity</label>
                  <select style={styles.input} {...register("SSD_Capacity")}>
                    {options.SSD_Capacity?.map((item) => (
                      <option key={item} value={item}>
                        {item}
                      </option>
                    ))}
                  </select>

                  <div style={styles.buttonContainer}>
                    <button style={styles.button} onClick={prevStep}>
                      Back
                    </button>
                    <button style={styles.button} onClick={nextStep}>
                      Next
                    </button>
                  </div>
                </div>
              )}

              {step === 5 && (
                <div>
                  <h2 style={styles.stepTitle}>Review & Submit</h2>
                  <pre style={styles.pre}>{JSON.stringify(watch(), null, 2)}</pre>

                  <div style={styles.buttonContainer}>
                    <button style={styles.button} onClick={prevStep}>
                      Back
                    </button>
                    <button style={styles.button} onClick={handleSubmit(onSubmit)}>
                      Submit
                    </button>
                  </div>
                </div>
              )}
            </motion.div>
          </AnimatePresence>
        </div>
      </div>
      {/* <div className="image"  style={styles.image}>
      <img src={Laptop} style={{
          
          transition: "transform 1s ease-in-out",
          transform: rotate ? "rotate(0deg)" : "rotate(405deg)",
        }} alt="" />
      </div> */}
      
      </div>
    </div>
  );
}

