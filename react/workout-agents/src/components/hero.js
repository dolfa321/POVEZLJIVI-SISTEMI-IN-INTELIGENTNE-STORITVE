function Hero() {
  return (
    <div className="relative w-full h-full overflow-hidden">
      {/* Zamegljeno ozadje */}
      <div
        className="absolute inset-0 bg-cover bg-center blur scale-110"
        style={{
          backgroundImage: `url('https://images.unsplash.com/photo-1554284126-aa88f22d8b74?auto=format&fit=crop&w=1400&q=80')`,
        }}
      />

      {/* Temen overlay čez ozadje */}
      <div className="absolute inset-0 bg-black/60 z-0" />

      {/* Vsebina */}
      <div className="relative z-10 w-full h-full flex flex-col justify-center items-center text-white text-center px-4 leading-tight">
        <h1 className="text-4xl md:text-6xl font-bold drop-shadow-lg mb-2 leading-snug">
          <span>Dobrodošli v svet</span>
          <br />
          <span>pametne vadbe</span>
        </h1>
        <p className="text-lg md:text-2xl max-w-xl drop-shadow-md mt-6 leading-snug">
        Naš agent vam pomaga analizirati učinkovitost treninga na podlagi srčnega utripa, intenzivnosti, razdalje in časa.
        <br />
            <span className="block mt-6 text-xl md:text-3xl font-semibold">
                Uporabite moč podatkov za boljše rezultate!
            </span>
        </p>
      </div>
    </div>
  );
}

export default Hero;
