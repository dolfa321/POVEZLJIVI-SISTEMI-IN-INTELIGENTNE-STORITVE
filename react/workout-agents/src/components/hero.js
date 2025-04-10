
function hero() {
  return (
    <div
      className="bg-cover bg-center h-[80vh] flex flex-col justify-center items-center text-white text-center px-4"
      style={{
        backgroundImage: `url('https://images.unsplash.com/photo-1554284126-aa88f22d8b74?auto=format&fit=crop&w=1400&q=80')`,
      }}
    >
      <h1 className="text-4xl md:text-5xl font-bold drop-shadow-lg mb-4">
        Dobrodošli v svet pametne vadbe 💪
      </h1>
      <p className="text-lg md:text-xl max-w-2xl drop-shadow-md">
        Naš agent vam pomaga analizirati učinkovitost treninga na podlagi
        srčnega utripa, intenzivnosti, razdalje in časa. Uporabite moč podatkov za boljše rezultate!
      </p>
    </div>
  );
}

export default hero;
