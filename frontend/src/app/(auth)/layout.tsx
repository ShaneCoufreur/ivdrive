import Image from "next/image";

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-iv-black flex items-center justify-center px-4 py-12">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -left-40 w-96 h-96 bg-iv-green/5 rounded-full blur-3xl" />
        <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-iv-cyan/5 rounded-full blur-3xl" />
      </div>

      <div className="relative z-10 w-full max-w-md flex flex-col items-center gap-8">
        <div className="flex items-center gap-3">
          <Image
            src="/logo.png"
            alt="iVDrive"
            width={40}
            height={40}
            className="rounded-lg"
            priority
          />
          <span className="text-2xl font-bold gradient-text tracking-tight">
            iVDrive
          </span>
        </div>

        {children}
      </div>
    </div>
  );
}
