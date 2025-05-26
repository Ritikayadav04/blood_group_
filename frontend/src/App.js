// import React from "react";
// import Upload from "./components/upload";
// import "./style.css";

// function App() {
//   return (
//     <div>
//       <Upload />
//     </div>
//   );
// }

// export default App;


import React, { useState, useEffect } from "react";
import axios from "axios";
import { Container, Card, Button, Form, Alert, Spinner } from "react-bootstrap";
import { ToastContainer, toast } from "react-toastify";
import { motion } from "framer-motion";
import "react-toastify/dist/ReactToastify.css";
import "./App.css";  // Import the new CSS file

function App() {
  const [image, setImage] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [refreshTimer, setRefreshTimer] = useState(null);

  const handleFileChange = (event) => {
    setImage(event.target.files[0]);
  };

  const handleUploadAndPredict = async () => {
    if (!image) {
      toast.error("Please select a fingerprint image.");
      return;
    }

    setError("");
    setPrediction(null);
    setLoading(true);

    const formData = new FormData();
    formData.append("image", image);

    try {
      await axios.post("http://127.0.0.1:8001/api/upload/", formData);
      toast.success("Image uploaded successfully!");

      const predictResponse = await axios.post("http://127.0.0.1:8001/api/predict/", formData);

      if (predictResponse.data.error) {
        setError(predictResponse.data.error);
        toast.error(predictResponse.data.error);
      } else {
        setPrediction(predictResponse.data.blood_group);
        toast.success(`Prediction successful! Blood Group: ${predictResponse.data.blood_group}`);

        const timer = setTimeout(() => {
          window.location.reload();
        }, 12000);

        setRefreshTimer(timer);
      }
    } catch (error) {
      setError("Failed to upload or predict. Please try again.");
      toast.error("Failed to upload or predict.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    return () => {
      if (refreshTimer) clearTimeout(refreshTimer);
    };
  }, [refreshTimer]);

  return (
    <Container className="container">
      <ToastContainer position="top-right" autoClose={3000} />

      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        <Card className="card-container">
          <Card.Body>
            <motion.h3 className="title" initial={{ y: -10 }} animate={{ y: 0 }} transition={{ duration: 0.5 }}>
              🔬 Blood Group Prediction
            </motion.h3>

            {error && <Alert variant="danger">{error}</Alert>}

            <Form>
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
                <Form.Group controlId="formFile" className="mb-3">
                  <Form.Label><strong>Select Fingerprint Image:</strong></Form.Label>
                  <Form.Control type="file" accept="image/*" onChange={handleFileChange} />
                </Form.Group>
              </motion.div>

              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}>
                <Button className="button" onClick={handleUploadAndPredict} disabled={loading}>
                  {loading ? <Spinner as="span" animation="border" size="sm" /> : "Upload & Predict"}
                </Button>
              </motion.div>
            </Form>

            {prediction && (
              <motion.div initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.6 }}>
                <Alert variant="success" className="mt-3 text-center">
                  🩸 <strong>Predicted Blood Group: {prediction}</strong>
                </Alert>
              </motion.div>
            )}
          </Card.Body>
        </Card>
      </motion.div>
    </Container>
  );
}

export default App;