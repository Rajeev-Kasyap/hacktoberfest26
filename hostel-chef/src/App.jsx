import React, { useState, useRef, useEffect } from 'react';
import { ChefHat, Microwave, Flame, Droplet, Camera, FileText, Loader2, ImagePlus, X, PenTool, PlusCircle, Timer, Eye, Skull, Smartphone } from 'lucide-react';


const EMPTY_EQUIP_MSGS = [
  "You need at least one weapon, unless you're cooking with sheer willpower.",
  "Select something. Or are you just going to stare at your food until it warms up?",
  "I cannot cook with literally nothing. Be so for real right now.",
  "Even a sad bowl counts. Click something.",
];

const EMPTY_INGRED_MSGS = [
  "Upload a photo or type something. I can't cook air.",
  "Are you fasting? Give me an ingredient.",
  "I know you're broke, but you must have SOMETHING.",
  "Look harder. Maybe check under your bed for a stray chip?",
];

const EQUIPMENTS = [
  { id: 'microwave', name: 'Microwave', icon: <Microwave className="w-5 h-5" />, desc: 'The radiation box' },
  { id: 'kettle', name: 'Electric Kettle', icon: <Droplet className="w-5 h-5" />, desc: 'For Maggi & tears' },
  { id: 'induction', name: 'Induction Stove', icon: <Flame className="w-5 h-5" />, desc: 'Probably banned' },
  { id: 'airfryer', name: 'Air Fryer', icon: <ChefHat className="w-5 h-5" />, desc: 'Oh, look at Mr. Rich' },
  { id: 'bowl', name: 'A Sad Bowl', icon: <Droplet className="w-5 h-5" />, desc: 'Unwashed since Tuesday' },
  { id: 'knife', name: 'A Knife', icon: <PenTool className="w-5 h-5" />, desc: 'Or just use your ID card' },
];

const LOADING_STEPS = [
  { text: "Letting the AI cook...", icon: ChefHat, color: "text-orange-500", anim: "animate-bounce" },
  { text: "Assuming you have salt (literally the bare minimum)...", icon: Flame, color: "text-zinc-400", anim: "animate-pulse" },
  { text: "Calculating the exact melting point of that cheese...", icon: Microwave, color: "text-yellow-400", anim: "animate-pulse" },
  { text: "Pouring water into the kettle...", icon: Droplet, color: "text-blue-400", anim: "animate-bounce" },
  { text: "Wait, no water. BRB, making a water cooler run...", icon: Timer, color: "text-amber-500", anim: "animate-spin" },
  { text: "Staring blankly at whatever this is...", icon: Eye, color: "text-zinc-300", anim: "animate-pulse" },
  { text: "Wondering why you bought these ingredients...", icon: Eye, color: "text-indigo-400", anim: "animate-bounce" },
  { text: "Consulting Gordon Ramsay's sleep paralysis demon...", icon: Skull, color: "text-red-500", anim: "animate-pulse" },
  { text: "Apologizing to your stomach in advance...", icon: Skull, color: "text-green-500", anim: "animate-bounce" },
  { text: "Googling 'can you die from eating raw oats'...", icon: Smartphone, color: "text-cyan-500", anim: "animate-pulse" },
  { text: "Negotiating with the hostel warden...", icon: Timer, color: "text-purple-500", anim: "animate-spin" },
  { text: "Almost there, hold back the Swiggy urge...", icon: Smartphone, color: "text-pink-500", anim: "animate-pulse" },
  { text: "Okay this is taking a while. AI is sweating...", icon: Loader2, color: "text-orange-500", anim: "animate-spin" },
];

export default function App() {
  const [step, setStep] = useState(1);
  const [equipment, setEquipment] = useState(new Set());
  const [inputMode, setInputMode] = useState(null); // 'photo' | 'text'
  const [ingredientsText, setIngredientsText] = useState('');
  const [images, setImages] = useState([]);
  
  
  const [isCooking, setIsCooking] = useState(false);
  const [loadingMsgIdx, setLoadingMsgIdx] = useState(0);
  const [equipError, setEquipError] = useState("");
  const [equipErrorIdx, setEquipErrorIdx] = useState(0);
  const [ingredError, setIngredError] = useState("");
  const [ingredErrorIdx, setIngredErrorIdx] = useState(0);
  
  const fileInputRef = useRef(null);

  const toggleEquipment = (id) => {
    setEquipment(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  

  const removeImage = (idx) => {
    setImages(prev => prev.filter((_, i) => i !== idx));
    setImageFiles(prev => prev.filter((_, i) => i !== idx));
  };

  // Cooking Animation Effect
  useEffect(() => {
    let interval;
    if (isCooking) {
      interval = setInterval(() => {
        setLoadingMsgIdx(prev => (prev + 1) % LOADING_STEPS.length);
      }, 3500); // Change message slower (every 3.5s) and loop continuously
    } else {
      setLoadingMsgIdx(0);
    }
    return () => clearInterval(interval);
  }, [isCooking]);

  const [recipeResult, setRecipeResult] = useState(null);

  const handleCook = async () => {
    setIsCooking(true);
    try {
      const formData = new FormData();
      formData.append('equipment', JSON.stringify(Array.from(equipment)));
      if (ingredientsText) {
        formData.append('ingredients_text', ingredientsText);
      }
      
      

      const response = await fetch('http://127.0.0.1:8000/api/cook', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      
      // Artificial delay so you can actually read the funny loading messages! 
      // (Localhost is too fast, it was skipping the 7-second animation)
      await new Promise(r => setTimeout(r, 6000));
      
      setRecipeResult(data);
      setStep(3); // Result step
    } catch (e) {
      console.error(e);
      alert('Failed to contact backend. Is uvicorn running?');
    } finally {
      setIsCooking(false);
    }
  };

  return (
    <div className="min-h-screen font-sans">
      {/* Header */}
      <header className="border-b border-zinc-800 bg-zinc-900/50 p-4 sticky top-0 backdrop-blur-md z-10">
        <div className="max-w-2xl mx-auto flex items-center gap-3">
          <div className="p-2 bg-orange-500/20 text-orange-400 rounded-lg">
            <ChefHat className="w-6 h-6" />
          </div>
          <div>
            <h1 className="font-black text-xl tracking-tight text-zinc-100">2 AM Hostel Chef</h1>
            <p className="text-xs font-medium text-zinc-400">Lower your expectations. Raise your sodium intake.</p>
          </div>
        </div>
      </header>

      <main className="max-w-2xl mx-auto p-4 sm:p-6 py-8">
        
        {/* STEP 1: Equipment */}
        {step === 1 && (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div>
              <h2 className="text-2xl font-black text-white mb-2">Step 1: Choose Your Weapons</h2>
              <p className="text-zinc-400 text-sm">
                What culinary contraband do you currently possess in your dorm room? Don't worry, I won't tell the warden.
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {EQUIPMENTS.map(eq => {
                const isSelected = equipment.has(eq.id);
                return (
                  <button
                    key={eq.id}
                    onClick={() => toggleEquipment(eq.id)}
                    className={`flex items-start gap-3 p-4 rounded-xl border-2 text-left transition-all ${
                      isSelected 
                        ? 'border-orange-500 bg-orange-500/10' 
                        : 'border-zinc-800 bg-zinc-900 hover:border-zinc-700 hover:bg-zinc-800/80'
                    }`}
                  >
                    <div className={`mt-0.5 ${isSelected ? 'text-orange-400' : 'text-zinc-500'}`}>
                      {eq.icon}
                    </div>
                    <div>
                      <h3 className={`font-bold ${isSelected ? 'text-orange-200' : 'text-zinc-300'}`}>{eq.name}</h3>
                      <p className={`text-xs mt-0.5 ${isSelected ? 'text-orange-400/80' : 'text-zinc-500'}`}>{eq.desc}</p>
                    </div>
                  </button>
                )
              })}
            </div>

            <div className="pt-4 border-t border-zinc-800 flex justify-end">
              <div className="flex flex-col items-end gap-2">
                {equipError && <span className="text-red-400 text-sm font-medium animate-in slide-in-from-right-4">{equipError}</span>}
                <button 
                  onClick={() => {
                    if (equipment.size === 0) {
                      setEquipError(EMPTY_EQUIP_MSGS[equipErrorIdx]);
                      setEquipErrorIdx((prev) => (prev + 1) % EMPTY_EQUIP_MSGS.length);
                    } else {
                      setEquipError("");
                      setStep(2);
                    }
                  }}
                  className="bg-orange-500 hover:bg-orange-400 text-black font-black px-6 py-3 rounded-xl transition"
                >
                  Next: The Ingredients &rarr;
                </button>
              </div>
            </div>
          </div>
        )}

        {/* STEP 2: Ingredients */}
        {step === 2 && !isCooking && (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div>
              <h2 className="text-2xl font-black text-white mb-2">Step 2: State of the Fridge</h2>
              <p className="text-zinc-400 text-sm">
                Show me the sad remains of your groceries. (Don't worry about Salt, we assume you have the bare minimum). Upload photos or type it out if you're too embarrassed to let an AI see your room.
              </p>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <button 
                onClick={() => setInputMode('photo')}
                className={`p-6 rounded-2xl border-2 flex flex-col items-center justify-center gap-3 transition ${
                  inputMode === 'photo' ? 'border-orange-500 bg-orange-500/10 text-orange-400' : 'border-zinc-800 bg-zinc-900 text-zinc-400 hover:border-zinc-700'
                }`}
              >
                <Camera className="w-8 h-8" />
                <span className="font-bold">Snap Photos</span>
              </button>
              <button 
                onClick={() => setInputMode('text')}
                className={`p-6 rounded-2xl border-2 flex flex-col items-center justify-center gap-3 transition ${
                  inputMode === 'text' ? 'border-orange-500 bg-orange-500/10 text-orange-400' : 'border-zinc-800 bg-zinc-900 text-zinc-400 hover:border-zinc-700'
                }`}
              >
                <FileText className="w-8 h-8" />
                <span className="font-bold">Type it out</span>
              </button>
            </div>

            {inputMode === 'photo' && (
              <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-8 text-center border-dashed">
                <input 
                  type="file" 
                  accept="image/*" 
                  capture="environment"
                  multiple
                  className="hidden" 
                  ref={fileInputRef}
                  onChange={handleImageUpload}
                />
                
                {images.length === 0 ? (
                  <>
                    <ImagePlus className="w-10 h-10 text-zinc-600 mx-auto mb-3" />
                    <p className="text-sm font-medium text-zinc-300 mb-4">Take photos of your desk/fridge items</p>
                    <button 
                      onClick={() => fileInputRef.current?.click()}
                      className="bg-zinc-800 hover:bg-zinc-700 text-white text-sm font-bold px-4 py-2 rounded-lg transition"
                    >
                      Open Camera / Gallery
                    </button>
                  </>
                ) : (
                  <div className="space-y-4">
                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                      {images.map((imgSrc, idx) => (
                        <div key={idx} className="relative group rounded-lg overflow-hidden border border-zinc-700 aspect-square">
                          <img src={imgSrc} alt={`Ingredient ${idx + 1}`} className="w-full h-full object-cover" />
                          <button 
                            onClick={() => removeImage(idx)}
                            className="absolute top-1 right-1 bg-black/60 p-1 rounded-full text-white hover:bg-red-500 transition opacity-0 group-hover:opacity-100"
                          >
                            <X className="w-4 h-4" />
                          </button>
                        </div>
                      ))}
                      <button 
                        onClick={() => fileInputRef.current?.click()}
                        className="rounded-lg border-2 border-dashed border-zinc-700 flex flex-col items-center justify-center gap-1 text-zinc-500 hover:text-zinc-300 hover:border-zinc-500 transition aspect-square"
                      >
                        <PlusCircle className="w-6 h-6" />
                        <span className="text-xs font-bold">Add More</span>
                      </button>
                    </div>
                  </div>
                )}
              </div>
            )}

            {inputMode === 'text' && (
              <div className="space-y-3">
                <label className="text-sm font-bold text-zinc-300">What do you have?</label>
                <textarea 
                  value={ingredientsText}
                  onChange={(e) => setIngredientsText(e.target.value)}
                  placeholder="e.g. Maggi, half a bag of stale Doritos, one slice of processed cheese, some sketchy ketchup..."
                  className="w-full bg-zinc-900 border border-zinc-800 rounded-xl p-4 text-zinc-100 placeholder:text-zinc-600 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent min-h-[120px] resize-none"
                />
              </div>
            )}

            <div className="pt-4 border-t border-zinc-800 flex justify-between">
              <button 
                onClick={() => setStep(1)}
                className="text-zinc-400 hover:text-white font-bold px-4 py-3 rounded-xl transition"
              >
                &larr; Back
              </button>
              <div className="flex flex-col items-end gap-2">
                {ingredError && <span className="text-red-400 text-sm font-medium animate-in slide-in-from-right-4">{ingredError}</span>}
                <button 
                  onClick={() => {
                    if (!ingredientsText && images.length === 0) {
                      setIngredError(EMPTY_INGRED_MSGS[ingredErrorIdx]);
                      setIngredErrorIdx((prev) => (prev + 1) % EMPTY_INGRED_MSGS.length);
                    } else {
                      setIngredError("");
                      handleCook();
                    }
                  }}
                  disabled={isCooking}
                  className="bg-orange-500 hover:bg-orange-400 text-black font-black px-6 py-3 rounded-xl flex items-center gap-2 disabled:opacity-50 transition"
                >
                  Cook Something Edible &rarr;
                </button>
              </div>
            </div>
          </div>
        )}

        {/* LOADING ANIMATION */}
        {isCooking && (
           <div className="flex flex-col items-center justify-center py-20 space-y-6 animate-in fade-in duration-300">
             <div className="relative h-20 flex items-center justify-center">
                {(() => {
                  const stepObj = LOADING_STEPS[loadingMsgIdx];
                  const IconComponent = stepObj.icon;
                  return (
                    <IconComponent className={`w-16 h-16 ${stepObj.color} ${stepObj.anim}`} />
                  );
                })()}
             </div>
             <div className="text-center">
               <h3 className="text-xl font-black text-white mb-2">AI is Cooking...</h3>
               <p className="text-orange-300 font-medium h-6 transition-all duration-300">
                 {LOADING_STEPS[loadingMsgIdx].text}
               </p>
             </div>
           </div>
        )}

        {/* STEP 3: Result (Dynamic from Backend) */}
        {step === 3 && recipeResult && (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
            <div className="text-center py-6">
              <div className="inline-block p-4 bg-emerald-500/20 text-emerald-400 rounded-full mb-4">
                <ChefHat className="w-10 h-10" />
              </div>
              <h2 className="text-3xl font-black text-white mb-2">{recipeResult.recipe_title}</h2>
              <p className="text-zinc-400 text-sm">
                {recipeResult.description}
              </p>
              <p className="text-zinc-600 text-[10px] mt-2 uppercase tracking-widest">{recipeResult.model_used}</p>
            </div>

            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6">
              <h3 className="text-orange-400 font-black mb-4 uppercase tracking-wider text-sm">Instructions</h3>
              <div className="space-y-4 text-zinc-300 text-sm">
                {recipeResult.steps.map((st, i) => (
                  <p key={i}>{st}</p>
                ))}
              </div>
            </div>

            <div className="pt-4 flex justify-center">
              <button 
                onClick={() => { setStep(1); setImages([]); setIngredientsText(''); setInputMode(null); setRecipeResult(null); }}
                className="text-orange-400 hover:text-orange-300 font-bold px-6 py-3 rounded-xl transition"
              >
                Restart / I survived
              </button>
            </div>
          </div>
        )}

      </main>
    </div>
  );
}
