import {useState} from 'react';
import Hero from '../components/hero';
import axios from 'axios'

function Home() {
    const [file, setFile] = useState(null);
    const [uploadMessage, setUploadMessage] = useState("");
    const [selectedWorkout, setSelectedWorkout] = useState("");
    const [data, setData] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = async () => {
        if (uploadMessage !== "") {
            setUploadMessage("")
        }
        if (!file || !selectedWorkout) {
            alert("Najprej izberi datoteko in vrsto vadbe!");
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        formData.append('workoutType', selectedWorkout);

        try {
            const response = await axios.post('http://localhost:5000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            console.log(response)
            setData(response.data)

            // const result = await response.json();
            // setUploadMessage(`✅ Odgovor strežnika: ${result.message}`);
            // setData(result)
            // console.print(result)
        } catch (error) {
            console.error("Napaka pri nalaganju:", error);
            const msg = error.response?.data?.error || "❌ Prišlo je do napake pri nalaganju datoteke.";
            setUploadMessage(msg);
        }
    };

    return (<div className="w-full h-screen overflow-hidden font-sans bg-gray-50 box-border">
        <div className="w-full h-full flex flex-row gap-0">

            {/* Leva stran - Hero komponenta */}
            <div className="w-1/3 h-full overflow-hidden">
                <Hero/>
            </div>

            {/* Sredina - Upload datoteke + Rezultati */}
            <div className="w-1/3 h-full flex flex-col items-center justify-center overflow-hidden px-4 gap-8">

                {/* Zgornji del - Upload datoteke */}
                <div className="bg-white border border-gray-300 rounded-xl p-6 shadow w-full max-w-sm box-border">
                    <h2 className="text-xl font-semibold mb-4 text-center leading-tight">
                        📤 Naloži svojo datoteko z vadbo
                    </h2>
                    <select
                        value={selectedWorkout}
                        onChange={(e) => setSelectedWorkout(e.target.value)}
                        className="mb-3 w-full border border-gray-300 rounded px-2 py-1"
                    >
                        <option value="">Izberi vrsto vadbe</option>
                        <option value="Cardio">Kardio</option>
                        <option value="Cycling">Kolesarjenje</option>
                        <option value="HIT">HIT</option>
                        <option value="Running">Tek</option>
                        <option value="Strength">Moč</option>
                        <option value="Yoga">Joga</option>
                    </select>
                    <input type="file" onChange={handleFileChange} className="mb-3" style={{marginLeft: "25%"}}/>
                    <button
                        onClick={handleUpload}
                        className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-1 px-4 rounded w-full"
                    >
                        Naloži
                    </button>
                    {uploadMessage && (<p className="text-green-600 mt-3 text-center">{uploadMessage}</p>)}
                </div>

                {/* Spodnji del - Rezultati analize (hardcoded for now) */}
                {data && (<div
                    className="bg-white border border-gray-300 rounded-xl p-6 shadow w-full max-w-sm box-border">
                    <h2 className="text-xl font-semibold mb-2 text-center">📊 Rezultat analize</h2>
                    <p className="text-sm text-gray-800 mb-4 text-center">
                        <strong>Your workout</strong> is in the <span
                        className="text-blue-600 font-semibold">{data.percentile}th</span> percentile.
                    </p>
                    <div className="text-sm text-gray-700 space-y-2">
                        <p><strong>💡 Recommendations:</strong></p>
                        {Object.entries(data.rec).map(([key, value]) => (<p key={key}>
                            <strong>{key.toString().toUpperCase()}:</strong> {value}
                        </p>))}
                    </div>
                </div>)}
            </div>

            {/* Desna stran - Tekst */}
            <div className="w-1/3 h-full flex flex-col justify-center px-4 overflow-hidden pt-8">
                <div className="overflow-auto min-h-0">
                    <h1 className="text-2xl font-bold mb-4 leading-tight">
                        🏃 Evaluator učinkovitosti treninga
                    </h1>

                    <p className="mb-4 leading-tight">
                        Dobrodošli v sistemu za analizo vaše vadbe! Naš informacijski agent vam pomaga oceniti, kako
                        učinkovita je bila vaša telesna aktivnost na podlagi fizioloških kazalnikov.
                    </p>

                    <p className="mb-4 leading-tight">
                        Uporabljamo modele nevronskih mrež, ki so bili naučeni na dejanskih podatkih, zbranih s
                        pametnimi zapestnicami.
                    </p>

                    <p className="mb-4 leading-tight">
                        Naložite svojo datoteko z vadbo in pridobite informacijo o tem, kako uspešni ste bili ter
                        kako lahko svojo učinkovitost še izboljšate.
                    </p>

                    {/* Cilj projekta */}
                    <h2 className="text-xl font-semibold mt-6 mb-2 text-blue-700">🎯 Cilj projekta</h2>
                    <p className="mb-4 leading-tight">
                        Razviti inteligentni sistem, ki na podlagi podatkov iz fitnes sledilnikov (npr. Apple Watch)
                        oceni intenzivnost in učinkovitost treninga.
                        Sistem temelji na nevronskih mrežah in fizioloških metrikah kot so srčni utrip, razdalja in
                        trajanje.
                    </p>

                    {/* Ključne formule */}
                    <h2 className="text-xl font-semibold mt-6 mb-2 text-blue-700">📐 Ključne formule</h2>
                    <ul className="list-disc list-inside space-y-2 text-sm">
                        <li><strong>HRmax:</strong> 208 − 0.7 × starost</li>
                        <li><strong>HR%:</strong> (HRavg ÷ HRmax) × 100</li>
                        <li><strong>TLI:</strong> HRavg × trajanje (v minutah)</li>
                        <li><strong>MET:</strong> (HRavg ÷ HRpočitek) × 3.5</li>
                        <li><strong>WEI:</strong> (HR% × razdalja) ÷ trajanje</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>);
}

export default Home;
