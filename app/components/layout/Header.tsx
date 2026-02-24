import React from 'react'; // Re-scan trigger
import {
    Search,
    User,
    Sun,
    Mail,
    TrendingUp,
    Youtube,
    Facebook,
    Instagram,
    Rss,
    Menu,
    ChevronDown,
    FileText
} from 'lucide-react';
import Link from 'next/link';

export default function Header() {
    return (
        <header className="flex flex-col w-full font-sans">
            {/* Top Bar - Deep Blue */}
            <div className="bg-[#00008B] text-white">
                <div className="max-w-[1330px] mx-auto px-4 h-20 flex items-center justify-between">
                    <div className="flex items-center gap-10">
                        {/* Left: Logo & Date */}
                        <div className="flex flex-col justify-center">
                            {/* Logo Simulation */}
                            <Link href="/" className="flex items-center gap-1 group">
                                {/* Colored Bars */}
                                <div className="flex gap-[2px] h-6 skew-x-[-15deg]">
                                    <div className="w-1.5 h-full bg-red-500"></div>
                                    <div className="w-1.5 h-full bg-yellow-400"></div>
                                    <div className="w-1.5 h-full bg-cyan-400"></div>
                                </div>
                                {/* Text */}
                                <span className="text-3xl font-black italic tracking-tighter ml-1">
                                    FOXIZ
                                </span>
                            </Link>
                            {/* Date */}
                            <div className="text-[10px] text-gray-300 mt-1 font-medium tracking-wide">
                                Monday, 23 Feb 2026
                            </div>
                        </div>

                        {/* Navigation */}
                        <nav className="hidden xl:flex items-center gap-1">
                            <Link
                                href="/"
                                className="bg-black text-white px-4 py-2 rounded-md font-bold text-sm hover:bg-gray-900 transition-colors"
                            >
                                Home
                            </Link>
                            <Link
                                href="/history"
                                className="px-4 py-2 font-bold text-sm hover:text-white/80 transition-opacity"
                            >
                                Read History
                            </Link>
                            <div className="flex items-center gap-1 px-4 py-2 font-bold text-sm cursor-pointer hover:text-white/80 transition-opacity">
                                Economic <ChevronDown size={14} />
                            </div>
                            <div className="flex items-center gap-1 px-4 py-2 font-bold text-sm cursor-pointer hover:text-white/80 transition-opacity">
                                Global Affairs <ChevronDown size={14} />
                            </div>
                            <div className="flex items-center gap-1 px-4 py-2 font-bold text-sm cursor-pointer hover:text-white/80 transition-opacity">
                                Pages <ChevronDown size={14} />
                            </div>
                            <Link
                                href="/blog"
                                className="px-4 py-2 font-bold text-sm hover:text-white/80 transition-opacity"
                            >
                                Blog
                            </Link>
                        </nav>
                    </div>

                    {/* Right: Actions */}
                    <div className="flex items-center gap-4">
                        <button className="bg-yellow-400 hover:bg-yellow-300 text-black px-4 py-2 rounded font-bold text-sm flex items-center gap-2 transition-colors">
                            <Mail size={16} />
                            Newsletter
                        </button>
                        <div className="flex items-center gap-3">
                            <button className="p-2 hover:bg-white/10 rounded-full transition-colors">
                                <User size={20} />
                            </button>
                            <button className="p-2 hover:bg-white/10 rounded-full transition-colors">
                                <Search size={20} />
                            </button>
                            <button className="p-2 hover:bg-white/10 rounded-full transition-colors">
                                <Sun size={20} />
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            {/* Bottom Bar - Bright Red */}
            <div className="bg-red-600 text-white overflow-hidden">
                <div className="max-w-[1330px] mx-auto px-4 h-10 flex items-center justify-between">
                    {/* Left: Trending/Scroller */}
                    <div className="flex items-center gap-4 overflow-x-auto no-scrollbar whitespace-nowrap ">
                        <div className="flex-shrink-0">
                            <TrendingUp size={16} className="stroke-[3]" />
                        </div>

                        <div className="flex items-center text-xs font-bold tracking-wide gap-3">
                            <Link href="/category/opinion" className="hover:underline">Opinion</Link>
                            <span className="text-white/50">/</span>
                            <Link href="/category/economic" className="hover:underline">Economic</Link>
                            <span className="text-white/50">/</span>
                            <Link href="/category/featured" className="hover:underline">Featured</Link>
                            <span className="text-white/50">/</span>
                            <Link href="/category/global-affairs" className="hover:underline">Global Affairs</Link>
                            <span className="text-white/50">/</span>
                            <Link href="/category/climate" className="hover:underline">Climate Change</Link>
                            <span className="text-white/50">/</span>
                            <Link href="/category/renewable" className="hover:underline">Renewable Energy</Link>
                            <span className="text-white/50">/</span>
                            <Link href="/category/politics" className="hover:underline">Politics</Link>
                            <span className="text-white/50">/</span>
                            <Link href="/category/research" className="hover:underline">Research</Link>
                        </div>
                    </div>

                    {/* Right: Social Icons */}
                    <div className="hidden md:flex items-center gap-4 pl-4 bg-red-600 relative z-10">
                        <Link href="#" className="hover:opacity-80 transition-opacity">
                            <Youtube size={16} fill="currentColor" />
                        </Link>
                        <Link href="#" className="hover:opacity-80 transition-opacity">
                            <div className="w-4 h-4 bg-white rounded-sm flex items-center justify-center text-red-600 font-black text-[10px]">G</div>
                            {/* Using a placeholder for Google News/similar as exact icon match might vary */}
                        </Link>
                        <Link href="#" className="hover:opacity-80 transition-opacity font-serif font-black italic">
                            M
                        </Link>
                        <Link href="#" className="hover:opacity-80 transition-opacity">
                            <Facebook size={16} fill="currentColor" />
                        </Link>
                        <Link href="#" className="hover:opacity-80 transition-opacity">
                            <Rss size={16} />
                        </Link>
                    </div>
                </div>
            </div>
        </header>
    );
}
