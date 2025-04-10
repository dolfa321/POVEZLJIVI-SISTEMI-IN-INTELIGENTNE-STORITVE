import { useState } from 'react';
import Hero from '../components/hero';

function Home() {
  const [file, setFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Najprej izberi datoteko!");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      setUploadMessage(`✅ Odgovor strežnika: ${result.message}`);
    } catch (error) {
      console.error("Napaka pri nalaganju:", error);
      setUploadMessage("❌ Prišlo je do napake pri nalaganju datoteke.");
    }
  };

  return (
    <div className="p-8 max-w-5xl mx-auto font-sans">
      <Hero/>
      <h1 className="text-3xl font-bold mb-4">🏃 Evaluator učinkovitosti treninga</h1>

      <p className="mb-4">
        Dobrodošli v sistemu za analizo vaše vadbe! Naš informacijski agent vam pomaga oceniti, kako učinkovita je bila vaša telesna aktivnost na podlagi fizioloških kazalnikov, kot so srčni utrip, razdalja, trajanje in dodatno izračunane metrike, kot so HR%, TLI, MET in WEI.
      </p>

      <p className="mb-4">
        Uporabljamo modele nevronskih mrež, ki so bili naučeni na dejanskih podatkih, zbranih s pametnimi zapestnicami (Apple Watch, Garmin, Fitbit ...). Sistem omogoča natančno povratno informacijo in personalizirana priporočila glede vaše vadbe.
      </p>

      <p className="mb-8">
        Naložite svojo datoteko z vadbo (CSV ali JSON) in pridobite informacijo o tem, kako uspešni ste bili ter kako lahko svojo učinkovitost še izboljšate.
      </p>

      <div className="bg-white border border-gray-300 rounded-xl p-6 shadow max-w-md">
        <h2 className="text-xl font-semibold mb-2">📤 Naloži svojo datoteko z vadbo</h2>
        <input type="file" onChange={handleFileChange} className="mb-2" />
        <button
          onClick={handleUpload}
          className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-1 px-4 rounded ml-2"
        >
          Naloži
        </button>
        {uploadMessage && (
          <p className="text-green-600 mt-3">{uploadMessage}</p>
        )}
      </div>

      <div className="mt-12">
        <h3 className="text-2xl font-bold mb-2">📊 Ključne formule za ocenjevanje vadbe</h3>
        <ul className="list-disc list-inside mb-6 space-y-1 text-gray-800">
          <li><strong>HRmax:</strong> 208 - 0.7 × starost</li>
          <li><strong>HR%:</strong> (HRavg / HRmax) × 100</li>
          <li><strong>TLI (Obremenitveni indeks):</strong> HRavg × trajanje (v minutah)</li>
          <li><strong>MET:</strong> (HRavg / HRpočitek) × 3.5</li>
          <li><strong>WEI (Indeks učinkovitosti):</strong> (HR% × razdalja) / trajanje</li>
        </ul>

        <p className="mb-4">
          Na osnovi teh vrednosti sistem statistično analizira intenzivnost in učinkovitost vašega treninga ter poda personalizirane predloge za napredek.
        </p>

        <p className="text-sm text-gray-600">
          📌 Razvit s pomočjo tehnologij: Python, TensorFlow, React in analize podatkov iz pametnih naprav.
        </p>
      </div>
    </div>
  );
}

export default Home;
